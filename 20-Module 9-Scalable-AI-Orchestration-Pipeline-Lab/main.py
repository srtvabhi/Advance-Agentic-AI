import sys

from graphs.pipeline_graph import build_pipeline_graph


DEFAULT_OBJECTIVE = (
    "Build a scalable AI orchestration pipeline for insurance claim intake. "
    "The system must process events from a queue, route high-risk claims, "
    "scale workers, and control latency and cost."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the scalable orchestration lab.
    print("Lab 20: Scalable AI Orchestration Pipeline\n")
    objective = input(f"Enter pipeline objective, or press Enter for default:\n{DEFAULT_OBJECTIVE}\n\nObjective: ").strip()
    objective = objective or DEFAULT_OBJECTIVE

    app = build_pipeline_graph()
    result = app.invoke(
        {
            "objective": objective,
            "events": [],
            "queue_summary": "",
            "routing_plan": "",
            "worker_pool_plan": "",
            "scaling_plan": "",
            "final_report": "",
        }
    )

    print("\n--- Queue Summary ---\n", result["queue_summary"])
    print("\n--- Routing Plan ---\n", result["routing_plan"])
    print("\n--- Worker Pool Plan ---\n", result["worker_pool_plan"])
    print("\n--- Scaling Plan ---\n", result["scaling_plan"])
    print("\n--- Final Pipeline Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()
