from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# This service manages the dummy incident-response PDF used in Lab 14.
# It can create the PDF from a source text file when missing, then read the PDF
# back page by page for chunking and retrieval.


# Function: create a simple PDF from the source runbook text file.
# Logic:
# 1. Create the PDF output folder if needed.
# 2. Read the incident runbook source text.
# 3. Write wrapped text lines into PDF pages.
# 4. Start a new page when the current page is full.
def create_pdf_from_text(source_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    text = source_path.read_text(encoding="utf-8")

    pdf = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setFont("Helvetica", 10)

    for paragraph in text.splitlines():
        for line in wrap(paragraph, width=95) or [""]:
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
            pdf.drawString(50, y, line)
            y -= 14
        y -= 6

    pdf.save()


# Function: make sure the runbook PDF exists before retrieval starts.
# Logic:
# If the PDF is missing, generate it from the source text so learners do not
# need to manually create a PDF before running the lab.
def ensure_pdf_exists(source_path: Path, pdf_path: Path) -> None:
    if not pdf_path.exists():
        create_pdf_from_text(source_path, pdf_path)


# Function: read text from each PDF page.
# Logic:
# 1. Open the PDF using PdfReader.
# 2. Extract text from each page.
# 3. Return page number and text pairs for chunking.
def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(pdf_path))
    return [
        (index, (page.extract_text() or "").strip())
        for index, page in enumerate(reader.pages, start=1)
    ]
