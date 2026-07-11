HIGH_RISK_TERMS = [
    "delete",
    "production",
    "payment",
    "customer data",
    "pii",
    "admin access",
    "refund",
    "database",
]

APPROVER_ROLES = {"security_admin", "compliance_manager", "platform_owner"}


def evaluate_approval(user_role: str, requested_action: str) -> tuple[str, bool, str]:
    # Decides whether an action requires a human approval checkpoint.
    lowered = requested_action.lower()
    is_high_risk = any(term in lowered for term in HIGH_RISK_TERMS)
    role_can_approve = user_role.lower() in APPROVER_ROLES

    if is_high_risk and not role_can_approve:
        return "high", True, "High-risk action requested by a role that cannot self-approve."

    if is_high_risk and role_can_approve:
        return "high", False, "High-risk action requested by an authorized approver role."

    return "low", False, "Low-risk action does not require human approval."


def create_approval_ticket(user_role: str, requested_action: str, reason: str) -> str:
    # Creates a simple simulated approval ticket.
    return (
        "APPROVAL-1001\n"
        f"Requested by: {user_role}\n"
        f"Action: {requested_action}\n"
        f"Reason: {reason}\n"
        "Status: Pending human approval"
    )


def execute_action(requested_action: str) -> str:
    # Simulates execution after approval checks are complete.
    return f"Action executed safely in simulation mode: {requested_action}"
