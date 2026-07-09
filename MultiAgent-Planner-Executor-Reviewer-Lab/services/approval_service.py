# Simple business rule service.
# In a real app, this could call ServiceNow, Jira, or an approval workflow API.


def approval_message(action: str) -> str:
    risky_words = ["production", "security", "payroll", "delete", "access", "customer email"]

    if any(word in action.lower() for word in risky_words):
        return "Human approval required before this action."

    return "No human approval required."

