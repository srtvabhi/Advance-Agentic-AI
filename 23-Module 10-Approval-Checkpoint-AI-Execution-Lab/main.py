import sys

from graphs.approval_graph import build_approval_graph


DEFAULT_ROLE = "support_agent"
DEFAULT_ACTION = "Delete old customer data from the production database after migration."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the approval checkpoint lab.
    print("Lab 23: Approval Checkpoints In AI Execution\n")
    role = input(f"Enter user role, or press Enter for default ({DEFAULT_ROLE}): ").strip() or DEFAULT_ROLE
    action = input(f"Enter requested action, or press Enter for default:\n{DEFAULT_ACTION}\n\nAction: ").strip() or DEFAULT_ACTION

    app = build_approval_graph()
    result = app.invoke(
        {
            "user_role": role,
            "requested_action": action,
            "risk_level": "",
            "approval_required": False,
            "approval_reason": "",
            "approval_ticket": "",
            "execution_result": "",
            "audit_record": "",
            "final_output": "",
        }
    )

    print("\n--- Risk Level ---\n", result["risk_level"])
    print("\n--- Approval Required ---\n", result["approval_required"])
    print("\n--- Approval Reason ---\n", result["approval_reason"])
    print("\n--- Approval Ticket ---\n", result["approval_ticket"])
    print("\n--- Execution Result ---\n", result["execution_result"])
    print("\n--- Audit Record ---\n", result["audit_record"])
    print("\n--- Final Explanation ---\n", result["final_output"])


if __name__ == "__main__":
    main()
