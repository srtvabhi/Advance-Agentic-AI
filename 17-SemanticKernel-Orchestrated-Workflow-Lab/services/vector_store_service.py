import chromadb

from config.settings import VECTOR_STORE_DIR, get_embedding_model
from models.rag_models import DocumentChunk, RetrievedChunk


COLLECTION_NAME = "sk_vendor_workflow_rag"


def create_embedding(openai_client, text: str) -> list[float]:
    response = openai_client.embeddings.create(model=get_embedding_model(), input=text)
    return response.data[0].embedding


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
        metadatas=[{"source": chunk.source, "page": chunk.page, "category": chunk.category} for chunk in chunks],
    )


def semantic_search(openai_client, query: str, top_k: int = 3) -> list[RetrievedChunk]:
    results = get_collection().query(
        query_embeddings=[create_embedding(openai_client, query)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    output = []
    for text, metadata, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        output.append(
            RetrievedChunk(
                text=text,
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                category=str(metadata["category"]),
                distance=float(distance),
            )
        )
    return output
