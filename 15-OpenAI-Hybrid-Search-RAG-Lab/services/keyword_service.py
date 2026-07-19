import re

from models.rag_models import DocumentChunk, SearchResult


# This service performs keyword search over product support chunks.
# Keyword search is useful for exact error terms such as "token expired",
# "cache mismatch", "webhook", or "settlement".


# Function: convert text into searchable lowercase terms.
# Logic:
# 1. Extract letters and numbers using a regular expression.
# 2. Lowercase all terms.
# 3. Return a set so overlap scoring is simple.
def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


# Function: find chunks that share exact terms with the user query.
# Logic:
# 1. Tokenize the user question.
# 2. Optionally skip chunks from other products.
# 3. Tokenize each chunk and calculate term overlap.
# 4. Score each result by overlap ratio.
# 5. Return highest keyword matches first.
def keyword_search(query: str, chunks: list[DocumentChunk], product_filter: str | None = None) -> list[SearchResult]:
    query_terms = tokenize(query)
    results = []

    for chunk in chunks:
        # Metadata filtering keeps AnalyticsPro and SecurePay guidance separate.
        if product_filter and chunk.product.lower() != product_filter.lower():
            continue

        chunk_terms = tokenize(chunk.text)
        overlap = query_terms.intersection(chunk_terms)
        if not overlap:
            continue

        # Simple score: how many query terms were found in this chunk.
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
