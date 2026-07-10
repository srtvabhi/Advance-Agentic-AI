import sys

from services.rag_pipeline import run_agentic_rag


DEFAULT_QUESTION = (
    "Can an employee book a business class flight for a 9 hour international trip, "
    "and what approval or receipt rules apply?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 13: OpenAI Multi-Step Agentic RAG Workflow\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    result = run_agentic_rag(question)
    print("\n" + result)


if __name__ == "__main__":
    main()
