import re

from models.rag_models import DocumentChunk, SearchResult


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def keyword_search(query: str, chunks: list[DocumentChunk], product_filter: str | None = None) -> list[SearchResult]:
    query_terms = tokenize(query)
    results = []

    for chunk in chunks:
        if product_filter and chunk.product.lower() != product_filter.lower():
            continue

        chunk_terms = tokenize(chunk.text)
        overlap = query_terms.intersection(chunk_terms)
        if not overlap:
            continue

        score = len(overlap) / max(len(query_terms), 1)
        results.append(
            SearchResult(
                text=chunk.text,
                source=chunk.source,
                page=chunk.page,
                category=chunk.category,
                product=chunk.product,
                score=score,
                search_type="keyword",
            )
        )

    return sorted(results, key=lambda item: item.score, reverse=True)
