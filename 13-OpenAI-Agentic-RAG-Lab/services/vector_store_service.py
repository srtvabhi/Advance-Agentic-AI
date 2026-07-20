import chromadb

from config.settings import VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, RetrievedChunk
from services.embedding_service import create_embedding


# This service manages ChromaDB, the local vector store for Lab 13.
# It stores embedded chunks from HR, Sales, and Marketing sources, then retrieves
# chunks that are closest in meaning to the user's question. Retrieval can also
# filter by business domain using chunk metadata.

COLLECTION_NAME = "agentic_rag_enterprise_knowledge"


# Function: create a ChromaDB client for this lab's local vector_store folder.
# Logic:
# 1. Ensure the vector_store folder exists.
# 2. Return a persistent ChromaDB client pointing to this lab folder only.
def get_chroma_client():
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))


# Function: get or create the ChromaDB collection.
# Logic:
# 1. Ensure the vector_store folder exists.
# 2. Open a persistent ChromaDB client.
# 3. Return the collection used by this lab.
def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


# Function: check whether the vector store already contains indexed chunks.
# Logic:
# 1. Open the existing ChromaDB collection if it exists.
# 2. Return True when documents are already stored.
# 3. Return False when the collection is missing or empty.
def has_existing_index() -> bool:
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False


# Function: delete the collection if a clean re-index is needed.
# Logic:
# Try to delete the collection, but ignore errors if it does not exist.
def reset_collection() -> None:
    client = get_chroma_client()
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
    if has_existing_index():
        print("Using existing ChromaDB vector store. Skipping re-indexing.")
        return

    collection = get_collection()

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
# 2. If a specific domain is selected, add a metadata filter.
# 3. Query ChromaDB for the nearest document chunks.
# 4. Convert raw ChromaDB results into RetrievedChunk objects.
# 5. Return those chunks to the RAG pipeline for answer generation.
def semantic_search(openai_client, query: str, category_filter: str = "All", top_k: int = 4) -> list[RetrievedChunk]:
    collection = get_collection()
    query_embedding = create_embedding(openai_client, query)
    query_arguments = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if category_filter != "All":
        query_arguments["where"] = {"category": category_filter}

    results = collection.query(**query_arguments)

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
