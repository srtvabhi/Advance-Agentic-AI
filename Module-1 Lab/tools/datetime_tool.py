from datetime import datetime

from agents import function_tool


@function_tool
def get_current_time() -> str:
    """Get the current local date and time."""
    print("[Tool called: get_current_time]")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
