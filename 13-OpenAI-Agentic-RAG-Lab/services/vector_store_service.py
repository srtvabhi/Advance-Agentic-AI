import chromadb

from config.settings import VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, RetrievedChunk
from services.embedding_service import create_embedding


# This service manages ChromaDB, the local vector store for Lab 13.
# It stores embedded document chunks and retrieves the chunks that are closest
# in meaning to the user's question.

COLLECTION_NAME = "agentic_rag_travel_policy"


# Function: get or create the ChromaDB collection.
# Logic:
# 1. Ensure the vector_store folder exists.
# 2. Open a persistent ChromaDB client.
# 3. Return the collection used by this lab.
def get_collection():
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME)


# Function: delete the collection if a clean re-index is needed.
# Logic:
# Try to delete the collection, but ignore errors if it does not exist.
def reset_collection() -> None:
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass


# Function: store document chunks in ChromaDB.
# Logic:
# 1. Get the collection.
# 2. Skip indexing if chunks already exist.
# 3. Create embeddings for each chunk.
# 4. Add chunk ids, text, embeddings, and metadata to ChromaDB.
def index_chunks(openai_client, chunks: list[DocumentChunk]) -> None:
    collection = get_collection()
    if collection.count() > 0:
        return

    embeddings = [create_embedding(openai_client, chunk.text) for chunk in chunks]
    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source": chunk.source,
                "page": chunk.page,
                "category": chunk.category,
            }
            for chunk in chunks
        ],
    )


# Function: find the most relevant chunks for a user question.
# Logic:
# 1. Convert the user question into an embedding.
# 2. Query ChromaDB for the nearest document chunks.
# 3. Convert raw ChromaDB results into RetrievedChunk objects.
# 4. Return those chunks to the RAG pipeline for answer generation.
def semantic_search(openai_client, query: str, top_k: int = 4) -> list[RetrievedChunk]:
    collection = get_collection()
    query_embedding = create_embedding(openai_client, query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append(
            RetrievedChunk(
                text=text,
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                category=str(metadata["category"]),
                distance=float(distance),
            )
        )
    return retrieved
