from models.resiliency_models import ResiliencyState
from services.dependency_service import call_primary_dependency
from services.llm_service import ask_model


def primary_node(state: ResiliencyState) -> ResiliencyState:
    # Calls the primary dependency and records whether retry or fallback is required.
    state["attempt"] += 1

    try:
        dependency_result = call_primary_dependency(state["task"], state["attempt"])
        state["primary_result"] = ask_model(
            "You are a production AI assistant.",
            (
                "Create a clear response using this successful dependency result.\n\n"
                f"Dependency result: {dependency_result}"
            ),
        )
        state["status"] = "primary_success"
    except Exception as exc:
        state["error_log"].append(f"Attempt {state['attempt']} failed: {exc}")
        if state["attempt"] < state["max_attempts"]:
            state["status"] = "retry_needed"
        else:
            state["status"] = "fallback_needed"

    return state


def route_after_primary(state: ResiliencyState) -> str:
    # Chooses the next LangGraph edge based on retry/fallback status.
    if state["status"] == "retry_needed":
        return "retry"
    if state["status"] == "fallback_needed":
        return "fallback"
    return "final"


def fallback_node(state: ResiliencyState) -> ResiliencyState:
    # Uses a fallback response path when the primary dependency is unavailable.
    state["fallback_result"] = ask_model(
        "You are a fallback AI assistant for a degraded production workflow.",
        (
            "The primary dependency failed. Create a safe fallback response. "
            "Mention that the workflow should continue in degraded mode, capture the task, "
            "notify operations, and retry later.\n\n"
            f"Task: {state['task']}\n"
            f"Errors: {state['error_log']}"
        ),
    )
    state["status"] = "fallback_success"
    return state


def final_node(state: ResiliencyState) -> ResiliencyState:
    # Creates the final resiliency report for the lab participant.
    state["final_answer"] = ask_model(
        "You are a reliability engineering trainer.",
        (
            "Explain the retry and fallback workflow used here. Include attempts, status, "
            "error log, final result, and production reliability lessons.\n\n"
            f"Task: {state['task']}\n"
            f"Status: {state['status']}\n"
            f"Primary result: {state['primary_result']}\n"
            f"Fallback result: {state['fallback_result']}\n"
            f"Error log: {state['error_log']}"
        ),
    )
    return state
