from semantic_kernel.functions import kernel_function

from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


class VendorRiskPlugin:
    """Native plugin for an orchestrated vendor risk workflow."""

    def __init__(self) -> None:
        self.openai_client = create_openai_client()
        self.source_file = SOURCE_DOCS_DIR / "vendor_risk_policy.txt"
        self.pdf_file = PDF_DIR / "vendor_risk_policy.pdf"
        self._ensure_index()

    def _ensure_index(self) -> None:
        ensure_pdf_exists(self.source_file, self.pdf_file)
        chunks = []
        for page, text in read_pdf_pages(self.pdf_file):
            chunks.extend(chunk_text(text, self.pdf_file.name, page, "vendor-risk"))
        index_chunks(self.openai_client, chunks)

    @kernel_function(name="classify_vendor", description="Classify vendor request risk from request text.")
    def classify_vendor(self, request: str) -> str:
        lowered = request.lower()
        if "customer data" in lowered or "payment" in lowered or "production" in lowered:
            return "High risk vendor request"
        if "internal" in lowered or "analytics" in lowered:
            return "Medium risk vendor request"
        return "Low risk vendor request"

    @kernel_function(name="retrieve_controls", description="Retrieve vendor risk controls from the policy PDF.")
    def retrieve_controls(self, request: str) -> str:
        results = semantic_search(self.openai_client, request, top_k=3)
        return "\n\n".join(f"Source: {item.citation()}\nContent: {item.text}" for item in results)

    @kernel_function(name="create_approval_task", description="Create a simulated approval task.")
    def create_approval_task(self, risk_level: str, vendor_name: str) -> str:
        return f"Created approval task VR-3107 for {vendor_name}. Risk level: {risk_level}."
