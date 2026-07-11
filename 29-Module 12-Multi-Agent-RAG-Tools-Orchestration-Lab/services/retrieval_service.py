from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "enterprise_policy_kb.txt"


def retrieve_policy_context(question: str, top_k: int = 2) -> str:
    # Performs simple keyword retrieval over the local policy knowledge base.
    documents = [item.strip() for item in DATA_FILE.read_text(encoding="utf-8").split("\n\n") if item.strip()]
    terms = {term.strip(".,?:;").lower() for term in question.split() if len(term) > 3}
    scored = []
    for document in documents:
        score = sum(1 for term in terms if term in document.lower())
        scored.append((score, document))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [document for score, document in scored[:top_k] if score > 0]
    return "\n\n".join(selected or documents[:top_k])
