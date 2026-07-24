import math
from typing import Any

from config.settings import create_openai_client, get_embedding_model


POLICY_DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "PROC-001",
        "title": "Purchase Approval Thresholds",
        "text": (
            "Purchases below USD 25,000 may be recommended after procurement analysis. "
            "Purchases of USD 25,000 or more require approval by a procurement manager. "
            "Purchases of USD 100,000 or more also require compliance review."
        ),
    },
    {
        "id": "SEC-014",
        "title": "Vendor Security Requirements",
        "text": (
            "Vendors processing confidential enterprise data must provide current security-assessment "
            "evidence, incident notification commitments, access controls, encryption details, "
            "and a data-retention schedule."
        ),
    },
    {
        "id": "PRIV-007",
        "title": "Personal Data and Cross-Border Processing",
        "text": (
            "Vendor proposals must not include unnecessary personal data. Cross-border personal-data "
            "processing requires an approved legal mechanism and documented data locations."
        ),
    },
    {
        "id": "COMP-021",
        "title": "Sanctions and Prohibited Vendors",
        "text": (
            "A purchase recommendation must be blocked when the vendor appears on the enterprise "
            "prohibited-vendor list or when required sanctions screening has not been completed."
        ),
    },
    {
        "id": "GOV-010",
        "title": "AI-Assisted Decision Governance",
        "text": (
            "AI output is advisory. High-impact, high-value, exception, or compliance-sensitive "
            "decisions require accountable human review. The workflow must retain source references, "
            "decision reasons, actor identity, and timestamps."
        ),
    },
]

PROHIBITED_VENDORS = {
    "Example Sanctioned Trading Ltd",
    "Blocked Supplier Corporation",
}

_POLICY_EMBEDDINGS: list[dict[str, Any]] = []


# Create one embedding for the supplied text using the lab's Azure OpenAI embedding model.
def create_embedding(text: str) -> list[float]:
    client = create_openai_client()
    response = client.embeddings.create(model=get_embedding_model(), input=text)
    return response.data[0].embedding


# Compute cosine similarity between two embedding vectors.
def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# Build policy embeddings once per Python process so repeated requests reuse them.
def ensure_policy_embeddings() -> None:
    global _POLICY_EMBEDDINGS
    if _POLICY_EMBEDDINGS:
        return

    embedded_documents: list[dict[str, Any]] = []
    for document in POLICY_DOCUMENTS:
        embedded = dict(document)
        embedded["embedding"] = create_embedding(document["title"] + "\n" + document["text"])
        embedded_documents.append(embedded)
    _POLICY_EMBEDDINGS = embedded_documents


# Retrieve approved policies that are most relevant to the procurement request.
def retrieve_policy_documents(query: str, top_k: int = 4) -> list[dict[str, Any]]:
    ensure_policy_embeddings()
    query_embedding = create_embedding(query)

    ranked: list[dict[str, Any]] = []
    for document in _POLICY_EMBEDDINGS:
        ranked.append(
            {
                "id": document["id"],
                "title": document["title"],
                "text": document["text"],
                "similarity": round(cosine_similarity(query_embedding, document["embedding"]), 4),
            }
        )

    ranked.sort(key=lambda item: item["similarity"], reverse=True)
    return ranked[:top_k]
