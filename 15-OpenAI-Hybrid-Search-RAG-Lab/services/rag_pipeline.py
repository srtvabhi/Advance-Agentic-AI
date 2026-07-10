from agents.hybrid_rag_agent import answer_with_hybrid_context, detect_product_filter
from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.keyword_service import keyword_search
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


SOURCE_FILE = SOURCE_DOCS_DIR / "product_support_kb.txt"
PDF_FILE = PDF_DIR / "product_support_kb.pdf"


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


def load_chunks() -> list:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
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


def build_index(client, chunks) -> None:
    index_chunks(client, chunks)


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


def run_hybrid_rag(question: str) -> str:
    client = create_openai_client()
    chunks = load_chunks()
    build_index(client, chunks)

    product_filter = detect_product_filter(question)
    semantic_results = semantic_search(client, question, product_filter=product_filter, top_k=4)
    keyword_results = keyword_search(question, chunks, product_filter=product_filter)
    final_results = deduplicate_results(semantic_results + keyword_results)
    answer = answer_with_hybrid_context(client, question, final_results)

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
