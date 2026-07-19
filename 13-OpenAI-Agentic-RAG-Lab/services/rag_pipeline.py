from config.settings import create_openai_client
from services.document_loader_service import load_enterprise_documents
from services.vector_store_service import index_chunks, semantic_search
from agents.rag_agent import create_retrieval_plan, generate_grounded_answer, select_data_domain


# This service is the main orchestration layer for Lab 13.
# It connects enterprise data loading, routing, vector indexing, retrieval
# planning, filtered semantic search, answer generation, and citation formatting.


# Function: build the ChromaDB index from HR, Sales, and Marketing data.
# Logic:
# 1. Load HR PDFs, Sales CSV rows, and Marketing campaign notes.
# 2. Convert each source into searchable chunks.
# 3. Store chunk embeddings and metadata in ChromaDB.
def build_index(openai_client) -> None:
    chunks = load_enterprise_documents()
    index_chunks(openai_client, chunks)


# Function: run the full Agentic RAG workflow for one user question.
# Logic:
# 1. Create the Azure OpenAI client.
# 2. Build or reuse the vector index.
# 3. Ask the model to select the best data domain.
# 4. Ask the model to create a retrieval plan for that domain.
# 5. Search ChromaDB using the selected domain as a metadata filter.
# 6. Generate a grounded answer using only retrieved context.
# 7. Return the domain, plan, answer, and citations as one formatted string.
def run_agentic_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    selected_domain = select_data_domain(client, question)
    plan = create_retrieval_plan(client, question, selected_domain)
    retrieved_chunks = semantic_search(client, question, category_filter=selected_domain, top_k=4)
    answer = generate_grounded_answer(client, question, selected_domain, plan, retrieved_chunks)

    citations = "\n".join(f"- {chunk.citation()}" for chunk in retrieved_chunks)
    return (
        f"--- Selected Data Domain ---\n{selected_domain}\n\n"
        f"--- Retrieval Plan ---\n{plan}\n\n"
        f"--- Answer ---\n{answer}\n\n"
        f"--- Retrieved Citations ---\n{citations}"
    )
