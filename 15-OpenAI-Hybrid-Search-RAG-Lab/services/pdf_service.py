from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# This service manages the product support PDF used in Lab 15.
# It can create the PDF from a source text file if needed, then read the PDF
# back page by page for product-aware chunking.


# Function: create a simple PDF from the product support source text.
# Logic:
# 1. Create the PDF output folder if it does not exist.
# 2. Read the source knowledge-base text.
# 3. Write wrapped text into PDF pages.
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


# Function: make sure the support PDF exists before indexing.
# Logic:
# If the PDF is missing, generate it from the source text file so the lab can
# run without manual PDF creation.
def ensure_pdf_exists(source_path: Path, pdf_path: Path) -> None:
    if not pdf_path.exists():
        create_pdf_from_text(source_path, pdf_path)


# Function: read text from every PDF page.
# Logic:
# 1. Open the PDF with PdfReader.
# 2. Extract text from each page.
# 3. Return page number and page text pairs.
def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(pdf_path))
    return [
        (index, (page.extract_text() or "").strip())
        for index, page in enumerate(reader.pages, start=1)
    ]
