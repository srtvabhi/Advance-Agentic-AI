from dataclasses import dataclass
from typing import Any, NotRequired, TypedDict


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    source: str
    page: int
    category: str


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int
    category: str
    distance: float

    def citation(self) -> str:
        return f"{self.source}, page {self.page}, category {self.category}"


class RAGObservabilityState(TypedDict):
    question: str
    selected_domain: NotRequired[str]
    retrieval_plan: NotRequired[str]
    retrieved_chunks: NotRequired[list[RetrievedChunk]]
    answer: NotRequired[str]
    evaluation: NotRequired[dict[str, Any]]
    metrics: NotRequired[list[dict[str, Any]]]
    estimated_tokens: NotRequired[dict[str, int]]
    retrieved_summary: NotRequired[list[dict[str, Any]]]
    final_output: NotRequired[str]
