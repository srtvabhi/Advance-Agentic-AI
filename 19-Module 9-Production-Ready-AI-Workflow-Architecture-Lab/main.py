import sys

from graphs.architecture_graph import build_architecture_graph


DEFAULT_PROBLEM = (
    "Design a production-ready AI workflow for an enterprise customer support assistant "
    "that handles 50,000 tickets per day, calls CRM tools, and needs high reliability."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 19: Production-Ready AI Workflow Architecture\n")
    problem = input(f"Enter architecture problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_architecture_graph()
    result = app.invoke(
        {
            "problem": problem,
            "intake_summary": "",
            "architecture_design": "",
            "deployment_pattern": "",
            "reliability_plan": "",
            "cost_latency_plan": "",
            "final_summary": "",
        }
    )

    print("\n--- Intake Summary ---\n", result["intake_summary"])
    print("\n--- Architecture Design ---\n", result["architecture_design"])
    print("\n--- Deployment Pattern ---\n", result["deployment_pattern"])
    print("\n--- Reliability Plan ---\n", result["reliability_plan"])
    print("\n--- Cost And Latency Plan ---\n", result["cost_latency_plan"])
    print("\n--- Final Production Summary ---\n", result["final_summary"])


if __name__ == "__main__":
    main()
