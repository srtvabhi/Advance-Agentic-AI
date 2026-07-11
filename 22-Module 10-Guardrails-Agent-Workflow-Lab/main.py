import sys

from graphs.guardrail_graph import build_guardrail_graph


DEFAULT_REQUEST = "Summarize our responsible AI policy for a new employee onboarding session."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the guardrails workflow lab.
    print("Lab 22: Guardrails In An AI Agent Workflow\n")
    request = input(f"Enter user request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST

    app = build_guardrail_graph()
    result = app.invoke(
        {
            "user_request": request,
            "classification": "",
            "risk_reason": "",
            "safe_prompt": "",
            "agent_answer": "",
            "audit_record": "",
            "final_output": "",
        }
    )

    print("\n--- Classification ---\n", result["classification"])
    print("\n--- Risk Reason ---\n", result["risk_reason"])
    print("\n--- Agent Answer ---\n", result["agent_answer"])
    print("\n--- Audit Record ---\n", result["audit_record"])
    print("\n--- Final Explanation ---\n", result["final_output"])


if __name__ == "__main__":
    main()
