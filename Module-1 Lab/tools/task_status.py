from agents import function_tool

from services.task_service import create_task_status


@function_tool
def get_task_status(task_name: str) -> str:
    """Create or check a task status in the simulated workflow tracker."""
    print(f"[Tool called: get_task_status({task_name})]")
    return create_task_status(task_name)
