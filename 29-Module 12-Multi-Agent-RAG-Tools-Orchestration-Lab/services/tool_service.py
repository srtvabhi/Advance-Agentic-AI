def create_ticket(title: str, priority: str) -> str:
    # Simulates creating an enterprise support ticket.
    return f"TICKET-2401 created with priority={priority}. Title: {title}"


def check_approval_required(action: str) -> str:
    # Simulates a governance tool that checks whether approval is required.
    risky_terms = ["production", "payroll", "customer data", "admin access", "delete"]
    if any(term in action.lower() for term in risky_terms):
        return "Approval required: manager approval, security approval, and audit ticket."
    return "Approval not required: low-risk request can proceed."


def run_enterprise_tools(user_request: str) -> str:
    # Calls simple deterministic tools based on the user request.
    priority = "High" if any(term in user_request.lower() for term in ["production", "admin", "payroll"]) else "Normal"
    ticket = create_ticket("Enterprise AI assistant request", priority)
    approval = check_approval_required(user_request)
    return f"{ticket}\n{approval}"
