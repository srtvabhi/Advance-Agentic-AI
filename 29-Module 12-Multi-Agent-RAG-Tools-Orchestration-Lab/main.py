import sys

from config.settings import configure_langsmith
from graphs.orchestration_graph import build_orchestration_graph


DEFAULT_REQUEST = (
    "A new engineering manager needs a laptop and temporary production admin access "
    "for a migration project. Create the enterprise workflow and identify approvals."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the multi-agent RAG and tools orchestration capstone.
    langsmith_enabled = configure_langsmith()
    print("Lab 29: Implement Multi-Agent Orchestration With RAG And Tools\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    request = input(f"Enter enterprise request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST

    app = build_orchestration_graph()
    result = app.invoke(
        {
            "user_request": request,
            "retrieved_context": "",
            "tool_results": "",
            "planner_output": "",
            "executor_output": "",
            "reviewer_output": "",
            "final_answer": "",
        }
    )

    print("\n--- Retrieved Context ---\n", result["retrieved_context"])
    print("\n--- Tool Results ---\n", result["tool_results"])
    print("\n--- Planner Agent ---\n", result["planner_output"])
    print("\n--- Executor Agent ---\n", result["executor_output"])
    print("\n--- Reviewer Agent ---\n", result["reviewer_output"])


if __name__ == "__main__":
    main()
