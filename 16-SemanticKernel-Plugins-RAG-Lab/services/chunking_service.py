from models.rag_models import DocumentChunk


def chunk_text(text: str, source: str, page: int, category: str) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1
    chunk_size = 600
    overlap = 100

    while start < len(words):
        end = start + chunk_size
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
        start = end - overlap
        chunk_number += 1

    return chunks
