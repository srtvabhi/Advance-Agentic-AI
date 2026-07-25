from time import perf_counter
from typing import Any, Callable, TypeVar

from langsmith import traceable

from models.rag_models import RetrievedChunk


T = TypeVar("T")


# Observability rule:
# Measure each workflow step locally so learners can compare terminal metrics
# with LangSmith trace spans.
def timed_step(step_name: str, action: Callable[[], T]) -> tuple[T, dict[str, Any]]:
    start = perf_counter()
    result = action()
    latency_ms = round((perf_counter() - start) * 1000, 2)
    return result, {"step": step_name, "latency_ms": latency_ms}


# Observability rule:
# LangSmith captures provider token usage on LangChain ChatOpenAI spans.
# This helper estimates token size for non-LLM text sections such as retrieved context.
def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


# Observability rule:
# Create a dedicated LangSmith span for token monitoring so learners can click
# this run and inspect token estimates as structured output.
@traceable(name="token_usage_estimation", run_type="chain")
def estimate_rag_token_usage(
    question: str,
    retrieval_plan: str,
    retrieved_context: str,
    final_answer: str,
) -> dict[str, int]:
    return {
        "question": estimate_tokens(question),
        "retrieval_plan": estimate_tokens(retrieval_plan),
        "retrieved_context": estimate_tokens(retrieved_context),
        "final_answer": estimate_tokens(final_answer),
        "total_estimated_tokens": estimate_tokens(question)
        + estimate_tokens(retrieval_plan)
        + estimate_tokens(retrieved_context)
        + estimate_tokens(final_answer),
    }


# Observability rule:
# Keep retrieval evidence visible. LangSmith should show which domain and
# source chunks were used before the answer was generated.
def summarize_retrieved_chunks(chunks: list[RetrievedChunk]) -> list[dict[str, Any]]:
    return [
        {
            "source": chunk.source,
            "page": chunk.page,
            "category": chunk.category,
            "distance": round(chunk.distance, 4),
        }
        for chunk in chunks
    ]


# Observability rule:
# Evaluate whether the final RAG answer appears grounded in retrieved context.
# This is intentionally simple for learners, but it creates useful LangSmith
# trace output for RAG quality review.
@traceable(name="rag_quality_evaluation", run_type="chain")
def evaluate_rag_response(
    question: str,
    selected_domain: str,
    retrieved_chunks: list[RetrievedChunk],
    answer: str,
) -> dict[str, Any]:
    answer_lower = answer.lower()
    citations = [chunk.citation() for chunk in retrieved_chunks]
    cited_sources = [
        citation
        for citation in citations
        if chunk_source_visible(citation, answer_lower)
    ]

    domain_mentioned = selected_domain.lower() in answer_lower or selected_domain == "All"
    has_retrieved_context = bool(retrieved_chunks)
    citation_score = round(len(cited_sources) / max(1, len(citations)), 2)
    groundedness_score = 1.0 if has_retrieved_context and citation_score > 0 else 0.5 if has_retrieved_context else 0.0
    relevance_score = 1.0 if domain_mentioned and has_retrieved_context else 0.5 if has_retrieved_context else 0.0
    overall_score = round((citation_score + groundedness_score + relevance_score) / 3, 2)

    return {
        "question": question,
        "selected_domain": selected_domain,
        "retrieved_chunk_count": len(retrieved_chunks),
        "citation_score": citation_score,
        "groundedness_score": groundedness_score,
        "relevance_score": relevance_score,
        "overall_score": overall_score,
        "passed": overall_score >= 0.6,
        "cited_sources": cited_sources,
        "expected_sources": citations,
    }


# Observability rule:
# A citation may include a path. Matching on the source file name is enough for
# this learner lab because answers usually cite short source names.
def chunk_source_visible(citation: str, answer_lower: str) -> bool:
    source_name = citation.split(",")[0].split("/")[-1].split("\\")[-1].lower()
    return source_name in answer_lower or citation.lower() in answer_lower


# Observability rule:
# Print a compact report so learners know what to look for in LangSmith.
def format_observability_report(
    metrics: list[dict[str, Any]],
    estimated_tokens: dict[str, int],
    retrieved_summary: list[dict[str, Any]],
    evaluation: dict[str, Any],
) -> str:
    latency_lines = "\n".join(
        f"- {item['step']}: {item['latency_ms']} ms"
        for item in metrics
    )
    token_lines = "\n".join(
        f"- {name}: {count}"
        for name, count in estimated_tokens.items()
    )
    retrieval_lines = "\n".join(
        f"- {item['category']} | {item['source']} | page {item['page']} | distance {item['distance']}"
        for item in retrieved_summary
    )
    return (
        "--- Observability Summary ---\n"
        f"LangSmith project: lab20_abhishek\n\n"
        "Latency by step:\n"
        f"{latency_lines}\n\n"
        "Estimated token usage:\n"
        f"{token_lines}\n\n"
        "Retrieved evidence:\n"
        f"{retrieval_lines or '- No chunks retrieved'}\n\n"
        "RAG quality evaluation:\n"
        f"- Overall score: {evaluation['overall_score']}\n"
        f"- Groundedness score: {evaluation['groundedness_score']}\n"
        f"- Citation score: {evaluation['citation_score']}\n"
        f"- Relevance score: {evaluation['relevance_score']}\n"
        f"- Passed: {evaluation['passed']}"
    )
