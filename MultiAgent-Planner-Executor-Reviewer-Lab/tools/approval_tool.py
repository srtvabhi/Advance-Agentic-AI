from agents import function_tool

from services.approval_service import approval_message


# Tool used by the executor agent to simulate human-in-the-loop approval.


@function_tool
def check_human_approval(action: str) -> str:
    """Check whether an action needs human approval."""
    print(f"[Tool called: check_human_approval({action})]")
    return approval_message(action)

