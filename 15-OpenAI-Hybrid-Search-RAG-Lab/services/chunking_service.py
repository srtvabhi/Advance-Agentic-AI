from models.rag_models import DocumentChunk


# This service splits product support knowledge-base text into searchable chunks.
# Each chunk keeps product metadata so retrieval can filter results for
# AnalyticsPro or SecurePay.


# Function: split product support text into overlapping chunks.
# Logic:
# 1. Split text into words.
# 2. Create chunks of 550 words.
# 3. Keep 90 words of overlap between chunks to preserve nearby context.
# 4. Store product metadata for product-specific filtering.
def chunk_text(text: str, source: str, page: int, category: str, product: str) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1
    chunk_size = 550
    overlap = 90

    while start < len(words):
        end = start + chunk_size

        # Store every chunk with source, page, category, and product so both
        # semantic search and keyword search can return useful citations.
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-{product}-p{page}-c{chunk_number}",
                text=" ".join(words[start:end]),
                source=source,
                page=page,
                category=category,
                product=product,
            )
        )
        if end >= len(words):
            break

        # Move the window forward, keeping overlap words from the previous chunk.
        start = end - overlap
        chunk_number += 1

    return chunks
