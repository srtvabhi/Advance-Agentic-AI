from typing import TypedDict


class RAGEvaluationState(TypedDict):
    # Shared state for RAG answer generation and evaluation.
    question: str
    retrieved_context: str
    answer: str
    evaluation: str
    observability_report: str
