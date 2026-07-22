from config.settings import create_agents_run_config, create_openai_client
from lab_agents.rag_agent import create_retrieval_plan, generate_grounded_answer, select_data_domain
from services.document_loader_service import load_enterprise_documents
from services.vector_store_service import has_existing_index, index_chunks, semantic_search


# This service is the main orchestration layer for Lab 13A.
# It connects enterprise data loading, routing, vector indexing, retrieval
# planning, separate vector-store search, answer generation, and citation formatting.


INDEX_READY = False


# Function: build the ChromaDB indexes from HR, Sales, and Marketing data.
# Logic:
# 1. Load HR PDFs, Sales CSV rows, and Marketing campaign notes.
# 2. Convert each source into searchable chunks.
# 3. Store each domain in its own ChromaDB vector-store folder.
def build_index(openai_client) -> None:
    global INDEX_READY

    if INDEX_READY:
        return

    if has_existing_index():
        print("Using existing HR, Sales, and Marketing vector stores. Skipping index build.")
        INDEX_READY = True
        return

    chunks = load_enterprise_documents()
    index_chunks(openai_client, chunks)
    INDEX_READY = True


# Function: run the full Agentic RAG workflow for one user question.
# Logic:
# 1. Create the Azure OpenAI client.
# 2. Build or reuse the separate vector indexes.
# 3. Ask the model to select the best data domain.
# 4. Ask the model to create a retrieval plan for that domain.
# 5. Search only the selected vector store, or all vector stores when domain is All.
# 6. Generate a grounded answer using only retrieved context.
# 7. Return the domain, plan, answer, and citations as one formatted string.
def run_agentic_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    selected_domain = select_data_domain(
        question,
        create_agents_run_config("Lab 13A - Domain Routing"),
    )
    plan = create_retrieval_plan(
        question,
        selected_domain,
        create_agents_run_config("Lab 13A - Retrieval Planning"),
    )
    retrieved_chunks = semantic_search(client, question, category_filter=selected_domain, top_k=4)
    answer = generate_grounded_answer(
        question,
        selected_domain,
        plan,
        retrieved_chunks,
        create_agents_run_config("Lab 13A - Grounded Answer"),
    )

    citations = "\n".join(f"- {chunk.citation()}" for chunk in retrieved_chunks)
    return (
        f"--- Selected Data Domain ---\n{selected_domain}\n\n"
        f"--- Retrieval Plan ---\n{plan}\n\n"
        f"--- Answer ---\n{answer}\n\n"
        f"--- Retrieved Citations ---\n{citations}"
    )
