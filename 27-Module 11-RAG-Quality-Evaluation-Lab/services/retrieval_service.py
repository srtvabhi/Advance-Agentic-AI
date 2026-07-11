from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "hr_policy_knowledge_base.txt"


def load_documents() -> list[str]:
    # Loads a tiny local knowledge base for the RAG evaluation lab.
    text = DATA_FILE.read_text(encoding="utf-8")
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def retrieve_context(question: str, top_k: int = 2) -> str:
    # Performs simple keyword retrieval so participants can focus on observability.
    documents = load_documents()
    question_terms = {term.strip(".,?:;").lower() for term in question.split() if len(term) > 3}

    scored = []
    for document in documents:
        document_lower = document.lower()
        score = sum(1 for term in question_terms if term in document_lower)
        scored.append((score, document))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [document for score, document in scored[:top_k] if score > 0]
    if not selected:
        selected = documents[:top_k]
    return "\n\n".join(selected)
