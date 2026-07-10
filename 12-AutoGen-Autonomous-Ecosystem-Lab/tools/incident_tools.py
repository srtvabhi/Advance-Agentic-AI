def check_service_health(service_name: str) -> str:
    """Check simulated service health."""
    return f"{service_name}: elevated latency detected, error rate 8%, database pool near capacity."


def create_incident_ticket(title: str, severity: str) -> str:
    """Create a simulated incident ticket."""
    return f"Created incident ticket INC-1042 with title '{title}' and severity '{severity}'."


def notify_response_team(message: str) -> str:
    """Notify a simulated response team."""
    return f"Notification sent to response team: {message}"

