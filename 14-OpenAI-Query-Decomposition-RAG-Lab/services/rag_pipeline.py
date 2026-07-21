from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_agents_run_config, create_openai_client
from lab_agents.decomposition_agent import decompose_question, synthesize_answer
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, search_for_sub_question


SOURCE_FILE = SOURCE_DOCS_DIR / "security_incident_runbook.txt"
PDF_FILE = PDF_DIR / "security_incident_runbook.pdf"


# This service orchestrates the full query decomposition RAG workflow.
# It builds the vector index, asks the model to split a complex question into
# smaller sub-questions, retrieves evidence for each sub-question, and then
# synthesizes one final answer.


# Function: build the vector index from the incident response runbook.
# Logic:
# 1. Ensure the PDF exists.
# 2. Read the PDF page by page.
# 3. Chunk each page as incident-response content.
# 4. Store chunk embeddings and metadata in ChromaDB.
def build_index(client) -> None:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(chunk_text(text, PDF_FILE.name, page, "incident-response"))
    index_chunks(client, chunks)


# Function: run the complete decomposition RAG pipeline.
# Logic:
# 1. Create the OpenAI client.
# 2. Build or reuse the vector index.
# 3. Decompose the original question into focused sub-questions.
# 4. Retrieve top chunks for each sub-question.
# 5. Synthesize the final answer from all retrieved evidence.
# 6. Return decomposed questions, final answer, and retrieval map.
def run_decomposition_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    sub_questions = decompose_question(
        question,
        create_agents_run_config("Lab 14 - Query Decomposition"),
    )
    retrieved = []
    for sub_question in sub_questions:
        retrieved.extend(search_for_sub_question(client, sub_question, top_k=2))

    answer = synthesize_answer(
        question,
        sub_questions,
        retrieved,
        create_agents_run_config("Lab 14 - Evidence Synthesis"),
    )
    sub_question_text = "\n".join(f"- {item}" for item in sub_questions)
    citations = "\n".join(f"- {chunk.sub_question}: {chunk.citation()}" for chunk in retrieved)

    return (
        f"--- Decomposed Questions ---\n{sub_question_text}\n\n"
        f"--- Final Answer ---\n{answer}\n\n"
        f"--- Retrieval Map ---\n{citations}"
    )
