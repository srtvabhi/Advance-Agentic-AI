import sys

from config.settings import configure_langsmith
from graphs.deployment_graph import build_deployment_graph


DEFAULT_WORKFLOW = (
    "Deploy a production enterprise agent workflow on Azure. The workflow uses LangGraph orchestration, "
    "RAG retrieval, ticket creation tools, approval checkpoints, RBAC security, LangSmith observability, "
    "and production scaling."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the deployment and evaluation capstone lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 30: Deploy And Evaluate An Enterprise AI Workflow Architecture\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    workflow = input(f"Enter workflow description, or press Enter for default:\n{DEFAULT_WORKFLOW}\n\nWorkflow: ").strip()
    workflow = workflow or DEFAULT_WORKFLOW

    app = build_deployment_graph()
    result = app.invoke(
        {
            "workflow_description": workflow,
            "deployment_plan": "",
            "evaluation_plan": "",
            "readiness_scorecard": "",
            "cost_performance_plan": "",
            "final_report": "",
        }
    )

    print("\n--- Deployment Plan ---\n", result["deployment_plan"])
    print("\n--- Evaluation Plan ---\n", result["evaluation_plan"])
    print("\n--- Readiness Scorecard ---\n", result["readiness_scorecard"])
    print("\n--- Cost And Performance Plan ---\n", result["cost_performance_plan"])


if __name__ == "__main__":
    main()
