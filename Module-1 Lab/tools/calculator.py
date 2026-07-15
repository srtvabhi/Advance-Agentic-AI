from agents import function_tool


@function_tool
def calculate(expression: str) -> str:
    """Calculate a simple arithmetic expression."""
    print(f"[Tool called: calculate({expression})]")

    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression. Use only numbers and + - * / ( )."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"
