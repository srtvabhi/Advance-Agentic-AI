def call_primary_dependency(task: str, attempt: int) -> str:
    # Simulates an unstable primary AI dependency.
    # The first attempt fails to demonstrate retry behavior.
    # If the task contains "force fallback", every primary attempt fails.
    if "force fallback" in task.lower():
        raise RuntimeError("Primary dependency is unavailable. Circuit breaker is open.")

    if attempt == 1:
        raise RuntimeError("Temporary timeout from primary dependency.")

    return f"Primary dependency completed the task after attempt {attempt}: {task}"
