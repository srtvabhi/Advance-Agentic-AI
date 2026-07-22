from pathlib import Path

from pypdf import PdfReader


# This service reads the existing PDF document used in the RAG lab.
# The PDF is the source of truth. The lab no longer creates a PDF from a text
# file, so learners practice a realistic PDF-first retrieval workflow.


# Function: confirm the required PDF file exists before indexing starts.
# Logic:
# 1. Check whether the PDF exists in the expected department folder.
# 2. Raise a clear error if the file is missing.
# 3. Continue only when the real PDF is available.
def validate_pdf_exists(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Required PDF not found: {pdf_path}. "
            "Place employee_travel_policy.pdf inside data/HR before running the lab."
        )


# Function: read text from every PDF page.
# Logic:
# 1. Confirm the PDF exists.
# 2. Open the PDF using PdfReader.
# 3. Extract text from each page.
# 4. Return a list of page number and page text pairs.
def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    validate_pdf_exists(pdf_path)
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    return pages
