import sys

from services.rag_pipeline import run_hybrid_rag


DEFAULT_QUESTION = (
    "For AnalyticsPro, what should support do when dashboard refresh fails "
    "with token expired and cache mismatch errors?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 15: OpenAI Hybrid Search RAG Pipeline\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    print("\n" + run_hybrid_rag(question))


if __name__ == "__main__":
    main()
