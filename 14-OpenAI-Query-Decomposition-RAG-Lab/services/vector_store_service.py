import chromadb

from config.settings import VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, RetrievedChunk
from services.embedding_service import create_embedding


COLLECTION_NAME = "query_decomposition_incident_rag"


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
            {"source": chunk.source, "page": chunk.page, "category": chunk.category}
            for chunk in chunks
        ],
    )


def search_for_sub_question(openai_client, sub_question: str, top_k: int = 2) -> list[RetrievedChunk]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[create_embedding(openai_client, sub_question)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append(
            RetrievedChunk(
                text=text,
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                category=str(metadata["category"]),
                distance=float(distance),
                sub_question=sub_question,
            )
        )
    return output
