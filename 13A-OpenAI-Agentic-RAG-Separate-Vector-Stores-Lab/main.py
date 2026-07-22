import sys

from services.rag_pipeline import run_agentic_rag


DEFAULT_QUESTION = (
    "Which sales region has the highest pipeline risk, and what action should the business take next?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 13A: OpenAI Agentic RAG with Separate Vector Stores\n")
    print("Type 'quit' or 'exit' to stop.")
    print(f"Press Enter to use the default question:\n{DEFAULT_QUESTION}\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in {"quit", "exit"}:
            print("Stopping Lab 13A.")
            break

        question = question or DEFAULT_QUESTION
        result = run_agentic_rag(question)
        print("\n" + result + "\n")


if __name__ == "__main__":
    main()
