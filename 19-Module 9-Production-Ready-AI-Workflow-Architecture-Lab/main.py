import sys
import uuid

from graphs.support_workflow_graph import build_support_workflow_graph


DEFAULT_TICKET = {
    "ticket_id": "T-1001",
    "customer_id": "C-001",
    "subject": "Possible duplicate charge",
    "body": "I see two subscription charges for the same month. Could you check what happened?",
    "channel": "web",
}


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_ticket_from_input() -> dict:
    print("Press Enter to use the default low-risk billing ticket.\n")
    subject = input(f"Subject [{DEFAULT_TICKET['subject']}]: ").strip() or DEFAULT_TICKET["subject"]
    body = input(f"Body [{DEFAULT_TICKET['body']}]: ").strip() or DEFAULT_TICKET["body"]
    channel = input(f"Channel [{DEFAULT_TICKET['channel']}]: ").strip() or DEFAULT_TICKET["channel"]

    return {
        "ticket_id": f"T-{uuid.uuid4().hex[:6].upper()}",
        "customer_id": "C-DEMO",
        "subject": subject,
        "body": body,
        "channel": channel,
        "errors": [],
        "trace": [],
        "retry_count": 0,
        "fallback_activated": False,
        "model_failures": [],
    }


def print_result(result: dict) -> None:
    print("\n--- Final Status ---")
    print(result["final_status"])

    print("\n--- Final Response ---")
    print(result["final_response"])

    print("\n--- Reliability Telemetry ---")
    print("Model target:", result.get("model_target", "not used"))
    print("Model used:", result.get("model_used", "not used"))
    print("Retries:", result.get("retry_count", 0))
    print("Fallback activated:", result.get("fallback_activated", False))
    print("Model failures:", len(result.get("model_failures", [])))

    print("\n--- Trace ---")
    for event in result.get("trace", []):
        print(f"{event['node']}: {event['status']}")


def main() -> None:
    print("Lab 19: Production-Ready Customer Support Workflow\n")
    ticket = build_ticket_from_input()
    workflow = build_support_workflow_graph()
    result = workflow.invoke(ticket)
    print_result(result)


if __name__ == "__main__":
    main()
