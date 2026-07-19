from models.rag_models import DocumentChunk


# This service splits long incident-response document text into smaller chunks.
# Query decomposition works better when each sub-question can retrieve focused
# chunks instead of searching one large document block.


# Function: split text into overlapping chunks.
# Logic:
# 1. Split the PDF page text into words.
# 2. Take 600 words per chunk.
# 3. Keep 100 words of overlap so context continues between chunks.
# 4. Store source, page, category, and chunk id for later citation.
def chunk_text(text: str, source: str, page: int, category: str) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1
    chunk_size = 600
    overlap = 100

    while start < len(words):
        end = start + chunk_size

        # Store each chunk as structured data so vector search and citations
        # can use the same source/page/category metadata later.
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-p{page}-c{chunk_number}",
                text=" ".join(words[start:end]),
                source=source,
                page=page,
                category=category,
            )
        )
        if end >= len(words):
            break

        # Move forward while preserving overlap words from the previous chunk.
        start = end - overlap
        chunk_number += 1

    return chunks
