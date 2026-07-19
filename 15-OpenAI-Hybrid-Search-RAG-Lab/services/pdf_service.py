from pathlib import Path

from pypdf import PdfReader


# This service reads the existing product support PDF used in Lab 15.
# The PDF is the source of truth for the hybrid search lab.


# Function: confirm the required PDF exists before indexing starts.
# Logic:
# 1. Check that data/pdfs/product_support_kb.pdf exists.
# 2. Raise a clear error if the PDF is missing.
# 3. Continue only when the real PDF source is available.
def validate_pdf_exists(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Required PDF not found: {pdf_path}. "
            "Place product_support_kb.pdf inside data/pdfs before running the lab."
        )


# Function: read text from every PDF page.
# Logic:
# 1. Confirm the PDF exists.
# 2. Open the PDF with PdfReader.
# 3. Extract text from each page.
# 4. Return page number and page text pairs.
def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    validate_pdf_exists(pdf_path)
    reader = PdfReader(str(pdf_path))
    return [
        (index, (page.extract_text() or "").strip())
        for index, page in enumerate(reader.pages, start=1)
    ]
