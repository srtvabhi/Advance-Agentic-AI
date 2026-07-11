import sys

from config.settings import configure_langsmith
from graphs.tracing_graph import build_tracing_graph


DEFAULT_INCIDENT = (
    "The enterprise HR chatbot is returning slow answers for payroll questions. "
    "Support tickets increased by 40 percent in the last hour."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the LangSmith workflow tracing lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 25: Trace An AI Agent Workflow Execution\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    incident = input(f"Enter incident, or press Enter for default:\n{DEFAULT_INCIDENT}\n\nIncident: ").strip()
    incident = incident or DEFAULT_INCIDENT

    app = build_tracing_graph()
    result = app.invoke(
        {
            "incident": incident,
            "triage_summary": "",
            "investigation_plan": "",
            "resolution_message": "",
            "trace_notes": "",
            "final_report": "",
        }
    )

    print("\n--- Triage Summary ---\n", result["triage_summary"])
    print("\n--- Investigation Plan ---\n", result["investigation_plan"])
    print("\n--- Resolution Message ---\n", result["resolution_message"])
    print("\n--- Trace Notes ---\n", result["trace_notes"])
    print("\n--- Final Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()
