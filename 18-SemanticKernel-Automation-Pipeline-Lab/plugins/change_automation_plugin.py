from semantic_kernel.functions import kernel_function

from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


class ChangeAutomationPlugin:
    """Native plugin for a multi-step IT change automation pipeline."""

    def __init__(self) -> None:
        self.openai_client = create_openai_client()
        self.source_file = SOURCE_DOCS_DIR / "change_management_standard.txt"
        self.pdf_file = PDF_DIR / "change_management_standard.pdf"
        self._ensure_index()

    def _ensure_index(self) -> None:
        ensure_pdf_exists(self.source_file, self.pdf_file)
        chunks = []
        for page, text in read_pdf_pages(self.pdf_file):
            chunks.extend(chunk_text(text, self.pdf_file.name, page, "change-management"))
        index_chunks(self.openai_client, chunks)

    @kernel_function(name="retrieve_standard", description="Retrieve change management rules from the PDF.")
    def retrieve_standard(self, change_request: str) -> str:
        results = semantic_search(self.openai_client, change_request, top_k=3)
        return "\n\n".join(f"Source: {item.citation()}\nContent: {item.text}" for item in results)

    @kernel_function(name="validate_change_type", description="Classify the IT change type.")
    def validate_change_type(self, change_request: str) -> str:
        lowered = change_request.lower()
        if "production" in lowered and ("firewall" in lowered or "database" in lowered):
            return "High risk standard change candidate"
        if "emergency" in lowered or "outage" in lowered:
            return "Emergency change"
        return "Normal change"

    @kernel_function(name="create_change_record", description="Create a simulated change record.")
    def create_change_record(self, change_type: str, summary: str) -> str:
        return f"Created change record CHG-5099. Type: {change_type}. Summary: {summary}"

    @kernel_function(name="send_notification", description="Send a simulated change notification.")
    def send_notification(self, message: str) -> str:
        return f"Notification sent to CAB and service owners: {message}"
