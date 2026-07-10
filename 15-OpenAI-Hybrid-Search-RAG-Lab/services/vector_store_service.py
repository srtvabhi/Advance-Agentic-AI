import chromadb

from config.settings import VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, SearchResult
from services.embedding_service import create_embedding


COLLECTION_NAME = "hybrid_support_rag"


def get_collection():
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME)


def index_chunks(openai_client, chunks: list[DocumentChunk]) -> None:
    collection = get_collection()
    if collection.count() > 0:
        return

    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=[create_embedding(openai_client, chunk.text) for chunk in chunks],
        metadatas=[
            {
                "source": chunk.source,
                "page": chunk.page,
                "category": chunk.category,
                "product": chunk.product,
            }
            for chunk in chunks
        ],
    )


def semantic_search(openai_client, query: str, product_filter: str | None = None, top_k: int = 4) -> list[SearchResult]:
    collection = get_collection()
    where_filter = {"product": product_filter} if product_filter else None
    results = collection.query(
        query_embeddings=[create_embedding(openai_client, query)],
        n_results=top_k,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append(
            SearchResult(
                text=text,
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                category=str(metadata["category"]),
                product=str(metadata["product"]),
                score=1 / (1 + float(distance)),
                search_type="semantic",
            )
        )
    return output
