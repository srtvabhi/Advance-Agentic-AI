import sys

from graphs.resiliency_graph import build_resiliency_graph


DEFAULT_TASK = (
    "Generate an executive incident summary for a payment API outage. "
    "Include customer impact, immediate mitigation, owner, and next review time."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the retry and fallback lab.
    print("Lab 21: Retry And Fallback Strategies\n")
    print("Tip: include 'force fallback' in the task to test the fallback path.\n")
    task = input(f"Enter production task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    app = build_resiliency_graph()
    result = app.invoke(
        {
            "task": task,
            "attempt": 0,
            "max_attempts": 2,
            "primary_result": "",
            "fallback_result": "",
            "final_answer": "",
            "error_log": [],
            "status": "not_started",
        }
    )

    print("\n--- Final Status ---\n", result["status"])
    print("\n--- Error Log ---")
    for error in result["error_log"]:
        print("-", error)
    print("\n--- Primary Result ---\n", result["primary_result"])
    print("\n--- Fallback Result ---\n", result["fallback_result"])
    print("\n--- Final Resiliency Report ---\n", result["final_answer"])


if __name__ == "__main__":
    main()
