import sys

from config.settings import configure_langsmith
from graphs.rag_eval_graph import build_rag_eval_graph


DEFAULT_QUESTION = "How quickly should payroll questions be handled, and when should HR requests be escalated?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the RAG quality evaluation lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 27: Evaluate RAG Response Quality With Observability\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    question = input(f"Enter RAG question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    app = build_rag_eval_graph()
    result = app.invoke(
        {
            "question": question,
            "retrieved_context": "",
            "answer": "",
            "evaluation": "",
            "observability_report": "",
        }
    )

    print("\n--- Retrieved Context ---\n", result["retrieved_context"])
    print("\n--- RAG Answer ---\n", result["answer"])
    print("\n--- LLM-As-Judge Evaluation ---\n", result["evaluation"])
    print("\n--- Observability Report ---\n", result["observability_report"])


if __name__ == "__main__":
    main()
