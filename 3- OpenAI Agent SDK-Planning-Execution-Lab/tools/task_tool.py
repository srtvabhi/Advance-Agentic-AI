from agents import function_tool

from services.task_service import task_status


# Tool 2: Task status
# The executor uses this tool to simulate workflow/task tracking.


@function_tool
def get_task_status(task_name: str) -> str:
    """Get the current status of a workflow task."""
    print(f"[Tool called: get_task_status({task_name})]")
    return task_status(task_name)

