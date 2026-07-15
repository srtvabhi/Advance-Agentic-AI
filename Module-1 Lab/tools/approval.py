from agents import function_tool

from services.approval_service import approval_decision


@function_tool
def check_approval_required(action: str) -> str:
    """Check whether an action requires human approval."""
    print(f"[Tool called: check_approval_required({action})]")
    return approval_decision(action)
