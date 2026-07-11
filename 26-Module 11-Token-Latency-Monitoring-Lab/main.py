import sys

from config.settings import configure_langsmith
from graphs.monitoring_graph import build_monitoring_graph


DEFAULT_REQUEST = "Write a short customer update explaining a delay in insurance claim processing."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the token and latency monitoring lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 26: Monitor Token Usage And Latency\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    request = input(f"Enter business request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST

    app = build_monitoring_graph()
    result = app.invoke(
        {
            "business_request": request,
            "draft_response": "",
            "reviewed_response": "",
            "telemetry": [],
            "monitoring_summary": "",
            "final_report": "",
        }
    )

    print("\n--- Draft Response ---\n", result["draft_response"])
    print("\n--- Reviewed Response ---\n", result["reviewed_response"])
    print("\n--- Step Telemetry ---")
    for item in result["telemetry"]:
        print(item)
    print("\n--- Monitoring Summary ---\n", result["monitoring_summary"])
    print("\n--- Final Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()
