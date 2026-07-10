from semantic_kernel.functions import kernel_function

from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


class HRPolicyPlugin:
    """Semantic Kernel native plugin for HR policy retrieval."""

    def __init__(self) -> None:
        self.openai_client = create_openai_client()
        self.source_file = SOURCE_DOCS_DIR / "hybrid_work_policy.txt"
        self.pdf_file = PDF_DIR / "hybrid_work_policy.pdf"
        self._ensure_index()

    def _ensure_index(self) -> None:
        ensure_pdf_exists(self.source_file, self.pdf_file)
        chunks = []
        for page, text in read_pdf_pages(self.pdf_file):
            chunks.extend(chunk_text(text, self.pdf_file.name, page, "hr-policy"))
        index_chunks(self.openai_client, chunks)

    @kernel_function(name="search_policy", description="Search the HR policy PDF for relevant policy context.")
    def search_policy(self, question: str) -> str:
        results = semantic_search(self.openai_client, question, top_k=3)
        return "\n\n".join(f"Source: {item.citation()}\nContent: {item.text}" for item in results)

    @kernel_function(name="create_hr_ticket", description="Create a simulated HR support ticket.")
    def create_hr_ticket(self, employee_name: str, request_summary: str) -> str:
        return f"Created HR ticket HR-2048 for {employee_name}: {request_summary}"
