from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search
from agents.rag_agent import create_retrieval_plan, generate_grounded_answer


SOURCE_FILE = SOURCE_DOCS_DIR / "employee_travel_policy.txt"
PDF_FILE = PDF_DIR / "employee_travel_policy.pdf"


def build_index(openai_client) -> None:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
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
