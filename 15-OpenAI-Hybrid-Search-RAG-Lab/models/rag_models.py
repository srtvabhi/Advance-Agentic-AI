from dataclasses import dataclass


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    source: str
    page: int
    category: str
    product: str


@dataclass
class SearchResult:
    text: str
    source: str
    page: int
    category: str
    product: str
    score: float
    search_type: str

    def citation(self) -> str:
        return f"{self.source}, page {self.page}, product {self.product}, category {self.category}"
