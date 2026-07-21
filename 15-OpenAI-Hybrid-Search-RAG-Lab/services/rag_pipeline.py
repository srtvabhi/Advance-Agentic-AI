from config.settings import PDF_DIR, create_agents_run_config, create_openai_client
from lab_agents.hybrid_rag_agent import answer_with_hybrid_context, detect_product_filter
from services.chunking_service import chunk_text
from services.keyword_service import keyword_search
from services.pdf_service import read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


PDF_FILE = PDF_DIR / "product_support_kb.pdf"


# This service orchestrates the full hybrid search RAG workflow.
# It combines semantic search, keyword search, product metadata filtering,
# result deduplication, and grounded answer generation.


# Function: extract the section of the support document for one product.
# Logic:
# 1. Find the product start marker.
# 2. For AnalyticsPro, stop before the SecurePay section.
# 3. For SecurePay, read from SecurePay marker to the end.
# 4. Return the original text if the marker is not found.
def product_section(text: str, product: str) -> str:
    if product == "AnalyticsPro":
        start_marker = "AnalyticsPro overview:"
        end_marker = "SecurePay overview:"
    else:
        start_marker = "SecurePay overview:"
        end_marker = ""

    start = text.find(start_marker)
    if start == -1:
        return text

    end = text.find(end_marker, start + len(start_marker)) if end_marker else -1
    if end == -1:
        return text[start:]
    return text[start:end]


# Function: load product-aware chunks from the PDF.
# Logic:
# 1. Read each page from the existing support PDF.
# 2. Create AnalyticsPro chunks with product metadata.
# 3. Create SecurePay chunks with product metadata.
def load_chunks() -> list:
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(
            chunk_text(
                product_section(text, "AnalyticsPro"),
                PDF_FILE.name,
                page,
                "support-kb",
                "AnalyticsPro",
            )
        )
        chunks.extend(
            chunk_text(
                product_section(text, "SecurePay"),
                PDF_FILE.name,
                page,
                "support-kb",
                "SecurePay",
            )
        )
    return chunks


# Function: build or reuse the ChromaDB vector index.
# Logic:
# Pass prepared chunks to the vector store service for embedding and indexing.
def build_index(client, chunks) -> None:
    index_chunks(client, chunks)


# Function: remove duplicate or near-duplicate search results.
# Logic:
# 1. Sort semantic and keyword results by score.
# 2. Use search type, source, page, product, and text prefix as a uniqueness key.
# 3. Keep the best unique results.
# 4. Return the top 5 results for final answer generation.
def deduplicate_results(results) -> list:
    seen = set()
    unique = []
    for item in sorted(results, key=lambda result: result.score, reverse=True):
        key = (item.search_type, item.source, item.page, item.product, item.text[:80])
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:5]


# Function: run the complete hybrid search RAG pipeline.
# Logic:
# 1. Create the OpenAI client.
# 2. Load product-aware chunks and build the vector index.
# 3. Detect product filter from the question.
# 4. Run semantic search against ChromaDB.
# 5. Run keyword search over chunks.
# 6. Merge and deduplicate both result sets.
# 7. Generate a grounded support answer.
def run_hybrid_rag(question: str) -> str:
    client = create_openai_client()
    run_config = create_agents_run_config("Lab 15 - Hybrid Search RAG")
    chunks = load_chunks()
    build_index(client, chunks)

    product_filter = detect_product_filter(question)
    semantic_results = semantic_search(client, question, product_filter=product_filter, top_k=4)
    keyword_results = keyword_search(question, chunks, product_filter=product_filter)
    final_results = deduplicate_results(semantic_results + keyword_results)
    answer = answer_with_hybrid_context(question, final_results, run_config)

    filter_text = product_filter or "No product metadata filter"
    result_map = "\n".join(
        f"- {item.search_type} score={item.score:.3f}: {item.citation()}"
        for item in final_results
    )
    return (
        f"--- Metadata Filter ---\n{filter_text}\n\n"
        f"--- Hybrid Search Results ---\n{result_map}\n\n"
        f"--- Answer ---\n{answer}"
    )
