import sys

from config.settings import configure_langsmith
from graphs.solution_graph import build_solution_graph


DEFAULT_PROBLEM = (
    "Design an enterprise Agentic AI assistant for employee services. "
    "It should answer HR and IT questions, retrieve policy documents, create support tickets, "
    "escalate risky requests, and provide observability for production operations."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the end-to-end enterprise solution capstone lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 28: Build An End-To-End Enterprise Agentic AI Solution\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    problem = input(f"Enter business problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_solution_graph()
    result = app.invoke(
        {
            "business_problem": problem,
            "requirements": "",
            "architecture": "",
            "security_compliance": "",
            "observability_governance": "",
            "production_readiness": "",
            "final_solution": "",
        }
    )

    print("\n--- Requirements ---\n", result["requirements"])
    print("\n--- Architecture ---\n", result["architecture"])
    print("\n--- Security And Compliance ---\n", result["security_compliance"])
    print("\n--- Observability And Governance ---\n", result["observability_governance"])
    print("\n--- Production Readiness ---\n", result["production_readiness"])


if __name__ == "__main__":
    main()
