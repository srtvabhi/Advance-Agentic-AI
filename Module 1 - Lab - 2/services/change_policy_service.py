def calculate_change_risk(change_summary: str, environment: str, business_impact: str) -> str:
    """Calculate a simple enterprise change-risk level."""
    text = f"{change_summary} {environment} {business_impact}".lower()
    score = 0

    high_risk_terms = ["production", "database", "payment", "security", "customer", "delete", "migration"]
    medium_risk_terms = ["api", "release", "integration", "authentication", "network"]

    score += sum(2 for term in high_risk_terms if term in text)
    score += sum(1 for term in medium_risk_terms if term in text)

    if score >= 5:
        return "High risk change. CAB approval, rollback plan, and business validation are required."
    if score >= 2:
        return "Medium risk change. Manager approval and rollback plan are required."
    return "Low risk change. Standard peer review and normal deployment checklist are sufficient."


def approval_policy(action: str) -> str:
    """Decide whether a change action requires human approval."""
    sensitive_terms = ["production", "database", "payment", "customer", "rollback", "security", "downtime"]

    if any(term in action.lower() for term in sensitive_terms):
        return f"Human approval required for: {action}"

    return f"Standard approval is sufficient for: {action}"


def maintenance_window(region: str) -> str:
    """Return a simulated maintenance window recommendation."""
    region_name = region.strip() or "global"
    return (
        f"Recommended maintenance window for {region_name}: "
        "Saturday 01:00-03:00 local time, with stakeholder notice 48 hours before change."
    )


def task_status(task_name: str) -> str:
    """Simulate enterprise task tracking."""
    return f"Task '{task_name}' created with status: Pending."
