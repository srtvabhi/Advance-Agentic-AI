from models.rag_models import DocumentChunk


# This service converts long document text into smaller searchable chunks.
# RAG systems use chunks because sending a full document to the model is slow,
# costly, and often less accurate than retrieving only the relevant sections.


# Function: split page text into overlapping chunks.
# Logic:
# 1. Split the page text into words.
# 2. Take chunk_size words at a time.
# 3. Keep overlap words between chunks so important context is not lost.
# 4. Store each chunk with source, page, category, and unique chunk_id.
def chunk_text(
    text: str,
    source: str,
    page: int,
    category: str,
    chunk_size: int = 650,
    overlap: int = 120,
) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_value = " ".join(chunk_words)

        # Create a structured chunk object so later services know where the
        # text came from and can show citations in the final answer.
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-p{page}-c{chunk_number}",
                text=chunk_text_value,
                source=source,
                page=page,
                category=category,
            )
        )
        if end >= len(words):
            break

        # Move forward but keep overlap words from the previous chunk.
        start = end - overlap
        chunk_number += 1

    return chunks
