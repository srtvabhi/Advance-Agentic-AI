import chromadb

from config.settings import VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, RetrievedChunk
from services.embedding_service import create_embedding


# This service manages ChromaDB for the query decomposition lab.
# It stores embedded incident runbook chunks and searches them separately for
# each decomposed sub-question.

COLLECTION_NAME = "query_decomposition_incident_rag"


# Function: get or create the ChromaDB collection for this lab.
# Logic:
# 1. Ensure the vector store folder exists.
# 2. Open a persistent ChromaDB client.
# 3. Return the collection used for incident-response retrieval.
def get_collection():
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME)


# Function: index incident response chunks in ChromaDB.
# Logic:
# 1. Get the collection.
# 2. Skip indexing if chunks already exist.
# 3. Create embeddings for all chunks.
# 4. Store chunk text and metadata for citation.
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


# Function: search the vector store for one decomposed sub-question.
# Logic:
# 1. Embed the sub-question.
# 2. Retrieve the closest incident-response chunks from ChromaDB.
# 3. Convert raw results into RetrievedChunk objects.
# 4. Attach the sub-question to each result for the retrieval map.
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
