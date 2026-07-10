from dataclasses import dataclass


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
    sub_question: str

    def citation(self) -> str:
        return f"{self.source}, page {self.page}, category {self.category}"
