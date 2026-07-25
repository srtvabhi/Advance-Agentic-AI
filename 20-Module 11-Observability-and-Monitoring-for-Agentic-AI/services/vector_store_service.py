import chromadb

from config.settings import HR_VECTOR_STORE_DIR, MARKETING_VECTOR_STORE_DIR, SALES_VECTOR_STORE_DIR
from models.rag_models import DocumentChunk, RetrievedChunk
from services.embedding_service import create_embedding


# This service manages one ChromaDB vector-store folder per business domain.
# HR, Sales, and Marketing are physically separated so learners can clearly see
# that the agent first chooses where to retrieve, then searches that data store.

COLLECTION_NAME = "domain_knowledge"

DOMAIN_STORE_DIRS = {
    "HR": HR_VECTOR_STORE_DIR,
    "Sales": SALES_VECTOR_STORE_DIR,
    "Marketing": MARKETING_VECTOR_STORE_DIR,
}


# Function: create a ChromaDB client for one business domain.
# Logic:
# 1. Find the vector-store folder for the requested domain.
# 2. Create the folder if it does not exist.
# 3. Return a persistent ChromaDB client for that domain only.
def get_chroma_client(domain: str):
    store_dir = DOMAIN_STORE_DIRS[domain]
    store_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(store_dir))


# Function: get or create the collection for one domain vector store.
# Logic:
# Each domain has its own ChromaDB folder, so the same collection name can be
# reused safely inside HR, Sales, and Marketing stores.
def get_collection(domain: str):
    client = get_chroma_client(domain)
    return client.get_or_create_collection(name=COLLECTION_NAME)


# Function: check whether all three vector stores already contain data.
# Logic:
# Return True only when HR, Sales, and Marketing collections all have documents.
def has_existing_index() -> bool:
    try:
        return all(get_collection(domain).count() > 0 for domain in DOMAIN_STORE_DIRS)
    except Exception:
        return False


# Function: store chunks in their domain-specific vector stores.
# Logic:
# 1. Group chunks by category: HR, Sales, Marketing.
# 2. Skip a domain if its vector store already contains documents.
# 3. Create embeddings and add only that domain's chunks to that domain's store.
def index_chunks(openai_client, chunks: list[DocumentChunk]) -> None:
    chunks_by_domain = {
        "HR": [chunk for chunk in chunks if chunk.category == "HR"],
        "Sales": [chunk for chunk in chunks if chunk.category == "Sales"],
        "Marketing": [chunk for chunk in chunks if chunk.category == "Marketing"],
    }

    for domain, domain_chunks in chunks_by_domain.items():
        collection = get_collection(domain)
        if collection.count() > 0:
            print(f"Using existing {domain} vector store. Skipping re-indexing.")
            continue

        if not domain_chunks:
            continue

        embeddings = [create_embedding(openai_client, chunk.text) for chunk in domain_chunks]
        collection.add(
            ids=[chunk.chunk_id for chunk in domain_chunks],
            documents=[chunk.text for chunk in domain_chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk.source,
                    "page": chunk.page,
                    "category": chunk.category,
                }
                for chunk in domain_chunks
            ],
        )


# Function: search one domain vector store.
# Logic:
# 1. Convert the question into an embedding.
# 2. Query only the selected domain's vector store.
# 3. Convert ChromaDB results into RetrievedChunk objects.
def search_domain(openai_client, query: str, domain: str, top_k: int) -> list[RetrievedChunk]:
    collection = get_collection(domain)
    if collection.count() == 0:
        return []

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


# Function: find relevant chunks from selected domain stores.
# Logic:
# 1. If selected domain is HR, Sales, or Marketing, search only that store.
# 2. If selected domain is All, search all stores and merge the best results.
# 3. Sort merged results by distance so the closest chunks appear first.
def semantic_search(openai_client, query: str, category_filter: str = "All", top_k: int = 4) -> list[RetrievedChunk]:
    if category_filter in DOMAIN_STORE_DIRS:
        return search_domain(openai_client, query, category_filter, top_k)

    retrieved = []
    for domain in DOMAIN_STORE_DIRS:
        retrieved.extend(search_domain(openai_client, query, domain, top_k))

    return sorted(retrieved, key=lambda chunk: chunk.distance)[:top_k]
