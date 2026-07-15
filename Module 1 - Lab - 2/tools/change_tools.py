from agents import function_tool

from services.change_policy_service import (
    approval_policy,
    calculate_change_risk,
    maintenance_window,
    task_status,
)


@function_tool
def assess_change_risk(change_summary: str, environment: str, business_impact: str) -> str:
    """Assess the risk level of an enterprise change request."""
    print("[Tool called: assess_change_risk]")
    return calculate_change_risk(change_summary, environment, business_impact)


@function_tool
def check_change_approval(action: str) -> str:
    """Check if a change action requires human approval."""
    print(f"[Tool called: check_change_approval({action})]")
    return approval_policy(action)


@function_tool
def recommend_maintenance_window(region: str) -> str:
    """Recommend a maintenance window for the change."""
    print(f"[Tool called: recommend_maintenance_window({region})]")
    return maintenance_window(region)


@function_tool
def create_change_task(task_name: str) -> str:
    """Create a simulated change-management task."""
    print(f"[Tool called: create_change_task({task_name})]")
    return task_status(task_name)
