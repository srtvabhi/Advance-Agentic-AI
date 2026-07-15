def approval_decision(action: str) -> str:
    """Return whether an action requires human approval."""
    sensitive_words = [
        "production",
        "delete",
        "database",
        "access",
        "payment",
        "security",
        "customer data",
    ]

    if any(word in action.lower() for word in sensitive_words):
        return f"Human approval required before completing this action: {action}"

    return f"No human approval required for this action: {action}"
