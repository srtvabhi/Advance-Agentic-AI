from agents.decomposition_agent import decompose_question, synthesize_answer
from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, search_for_sub_question


SOURCE_FILE = SOURCE_DOCS_DIR / "security_incident_runbook.txt"
PDF_FILE = PDF_DIR / "security_incident_runbook.pdf"


def build_index(client) -> None:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(chunk_text(text, PDF_FILE.name, page, "incident-response"))
    index_chunks(client, chunks)


def run_decomposition_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    sub_questions = decompose_question(client, question)
    retrieved = []
    for sub_question in sub_questions:
        retrieved.extend(search_for_sub_question(client, sub_question, top_k=2))

    answer = synthesize_answer(client, question, sub_questions, retrieved)
    sub_question_text = "\n".join(f"- {item}" for item in sub_questions)
    citations = "\n".join(f"- {chunk.sub_question}: {chunk.citation()}" for chunk in retrieved)

    return (
        f"--- Decomposed Questions ---\n{sub_question_text}\n\n"
        f"--- Final Answer ---\n{answer}\n\n"
        f"--- Retrieval Map ---\n{citations}"
    )
