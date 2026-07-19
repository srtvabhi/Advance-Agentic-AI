from config.settings import PDF_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search
from agents.rag_agent import create_retrieval_plan, generate_grounded_answer


# This service is the main orchestration layer for Lab 13.
# It connects PDF reading, chunking, vector indexing, retrieval planning,
# semantic search, answer generation, and citation formatting.

PDF_FILE = PDF_DIR / "employee_travel_policy.pdf"


# Function: build the ChromaDB index from the travel policy PDF.
# Logic:
# 1. Read the existing travel policy PDF page by page.
# 2. Split each page into overlapping chunks.
# 3. Store chunk embeddings and metadata in ChromaDB.
def build_index(openai_client) -> None:
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(
            chunk_text(
                text=text,
                source=PDF_FILE.name,
                page=page,
                category="travel-policy",
            )
        )
    index_chunks(openai_client, chunks)


# Function: run the full Agentic RAG workflow for one user question.
# Logic:
# 1. Create the Azure OpenAI client.
# 2. Build or reuse the vector index.
# 3. Ask the model to create a retrieval plan.
# 4. Search ChromaDB for relevant document chunks.
# 5. Generate a grounded answer using only retrieved context.
# 6. Return the plan, answer, and citations as one formatted string.
def run_agentic_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    plan = create_retrieval_plan(client, question)
    retrieved_chunks = semantic_search(client, question, top_k=4)
    answer = generate_grounded_answer(client, question, plan, retrieved_chunks)

    citations = "\n".join(f"- {chunk.citation()}" for chunk in retrieved_chunks)
    return (
        f"--- Retrieval Plan ---\n{plan}\n\n"
        f"--- Answer ---\n{answer}\n\n"
        f"--- Retrieved Citations ---\n{citations}"
    )
