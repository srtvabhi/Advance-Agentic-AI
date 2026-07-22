import csv
from pathlib import Path

from config.settings import HR_DIR, MARKETING_DIR, SALES_DIR
from models.rag_models import DocumentChunk
from services.chunking_service import chunk_text
from services.pdf_service import read_pdf_pages


# This service loads enterprise knowledge from three business folders:
# HR has PDF policy documents, Sales has CSV pipeline data, and Marketing has
# campaign notes. The RAG pipeline indexes all of them into ChromaDB.


# Function: load HR PDF documents.
# Logic:
# 1. Find every PDF in data/HR.
# 2. Read each PDF page.
# 3. Split page text into chunks tagged with category HR.
def load_hr_documents() -> list[DocumentChunk]:
    chunks = []
    for pdf_file in HR_DIR.glob("*.pdf"):
        for page, text in read_pdf_pages(pdf_file):
            chunks.extend(
                chunk_text(
                    text=text,
                    source=f"HR/{pdf_file.name}",
                    page=page,
                    category="HR",
                )
            )
    return chunks


# Function: load Sales CSV records.
# Logic:
# 1. Read each CSV row from data/Sales.
# 2. Convert the row into readable business text.
# 3. Store each row as a searchable chunk tagged with category Sales.
def load_sales_documents() -> list[DocumentChunk]:
    chunks = []
    for csv_file in SALES_DIR.glob("*.csv"):
        with csv_file.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader, start=1):
                row_text = "; ".join(f"{key}: {value}" for key, value in row.items())
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"Sales/{csv_file.name}-row-{row_number}",
                        text=f"Sales pipeline record. {row_text}",
                        source=f"Sales/{csv_file.name}",
                        page=row_number,
                        category="Sales",
                    )
                )
    return chunks


# Function: load Marketing campaign documents.
# Logic:
# 1. Read text and markdown files from data/Marketing.
# 2. Split the campaign notes into chunks.
# 3. Tag each chunk with category Marketing.
def load_marketing_documents() -> list[DocumentChunk]:
    chunks = []
    for text_file in list(MARKETING_DIR.glob("*.txt")) + list(MARKETING_DIR.glob("*.md")):
        text = text_file.read_text(encoding="utf-8")
        chunks.extend(
            chunk_text(
                text=text,
                source=f"Marketing/{text_file.name}",
                page=1,
                category="Marketing",
            )
        )
    return chunks


# Function: load all enterprise documents from HR, Sales, and Marketing.
# Logic:
# Combine all domain-specific loaders into one list for vector indexing.
def load_enterprise_documents() -> list[DocumentChunk]:
    return load_hr_documents() + load_sales_documents() + load_marketing_documents()
