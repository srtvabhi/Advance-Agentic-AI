from models.rag_models import DocumentChunk


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
        start = end - overlap
        chunk_number += 1

    return chunks
