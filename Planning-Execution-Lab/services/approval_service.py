# Service files contain business logic behind tools.
# In a real enterprise app, this could call ServiceNow, Jira, Workday, or an approval API.


def approval_decision(action: str) -> str:
    high_risk_words = [
        "access",
        "admin",
        "production",
        "payment",
        "delete",
        "security",
        "hr record",
        "payroll",
    ]

    if any(word in action.lower() for word in high_risk_words):
        return "Human approval required before this action can be completed."

    return "No human approval required. This action can continue."

