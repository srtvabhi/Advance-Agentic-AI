from datetime import datetime

from agents import function_tool


# Tool 2: Date and time
# This tool returns the current local system date and time.


@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    print("[Tool called: get_current_time]")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

