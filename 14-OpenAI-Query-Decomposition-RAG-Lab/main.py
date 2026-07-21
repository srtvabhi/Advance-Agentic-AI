import sys

from services.rag_pipeline import run_decomposition_rag


DEFAULT_QUESTION = (
    "A suspicious login was followed by data export from a finance system. "
    "What should the response team do first, how should severity be assigned, "
    "and what evidence must be preserved?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 14: OpenAI Query Decomposition RAG\n")
    print("Enter a question, press Enter for the default question, or type 'quit' to exit.")

    while True:
        question = input(f"\nDefault question:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()

        if question.casefold() == "quit":
            print("Exiting Lab 14.")
            break

        question = question or DEFAULT_QUESTION
        print("\n" + run_decomposition_rag(question))


if __name__ == "__main__":
    main()
