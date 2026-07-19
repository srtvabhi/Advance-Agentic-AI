from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# This service handles the dummy PDF document used in the RAG lab.
# It can create a PDF from the source text file and read text back from each
# PDF page so the content can be chunked and indexed.


# Function: create a simple PDF from a text file.
# Logic:
# 1. Create the PDF output folder if it does not exist.
# 2. Read the source .txt policy file.
# 3. Write wrapped text lines into a PDF page.
# 4. Start a new PDF page when the current page is full.
def create_pdf_from_text(source_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    text = source_path.read_text(encoding="utf-8")
    pdf = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    y = height - 50

    pdf.setFont("Helvetica", 10)
    for paragraph in text.splitlines():
        lines = wrap(paragraph, width=95) or [""]
        for line in lines:
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
            pdf.drawString(50, y, line)
            y -= 14
        y -= 6

    pdf.save()


# Function: make sure the PDF exists before the RAG pipeline reads it.
# Logic:
# If the PDF is missing, generate it from the source text file.
def ensure_pdf_exists(source_path: Path, pdf_path: Path) -> None:
    if not pdf_path.exists():
        create_pdf_from_text(source_path, pdf_path)


# Function: read text from every PDF page.
# Logic:
# 1. Open the PDF using PdfReader.
# 2. Extract text from each page.
# 3. Return a list of page number and page text pairs.
def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    return pages
