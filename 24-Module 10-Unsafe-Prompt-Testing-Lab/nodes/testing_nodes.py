from models.testing_models import PromptTestState
from services.llm_service import ask_model
from services.prompt_test_service import evaluate_prompt, load_default_prompts, summarize_results


def _sanitized_results(results: list[dict]) -> list[dict]:
    # Removes raw unsafe prompt text before sending summaries to the LLM.
    sanitized = []
    for index, result in enumerate(results, start=1):
        sanitized.append(
            {
                "case": f"test_case_{index}",
                "decision": result["decision"],
                "reason": result["reason"],
            }
        )
    return sanitized


def load_tests_node(state: PromptTestState) -> PromptTestState:
    # Loads the unsafe prompt test cases.
    if not state["prompts"]:
        state["prompts"] = load_default_prompts()
    return state


def run_tests_node(state: PromptTestState) -> PromptTestState:
    # Runs deterministic safety checks against every prompt.
    results = [evaluate_prompt(prompt) for prompt in state["prompts"]]
    blocked, allowed = summarize_results(results)
    state["test_results"] = results
    state["blocked_count"] = blocked
    state["allowed_count"] = allowed
    return state


def improvement_plan_node(state: PromptTestState) -> PromptTestState:
    # Uses the model to create a practical guardrail improvement plan.
    sanitized_results = _sanitized_results(state["test_results"])
    state["improvement_plan"] = ask_model(
        "You are an enterprise AI safety engineer.",
        (
            "Create a short improvement plan based on these unsafe prompt test results. "
            "Include prompt injection defense, privacy controls, moderation, and audit logging.\n\n"
            f"Sanitized results: {sanitized_results}"
        ),
    )
    return state


def final_report_node(state: PromptTestState) -> PromptTestState:
    # Creates the final test report for participants.
    sanitized_results = _sanitized_results(state["test_results"])
    state["final_report"] = ask_model(
        "You are a responsible AI workshop trainer.",
        (
            "Explain the unsafe prompt testing results in simple terms. "
            "Mention how many prompts were blocked and allowed, and summarize the improvement plan.\n\n"
            f"Suite: {state['test_suite_name']}\n"
            f"Blocked: {state['blocked_count']}\n"
            f"Allowed: {state['allowed_count']}\n"
            f"Sanitized results: {sanitized_results}\n"
            f"Improvement plan: {state['improvement_plan']}"
        ),
    )
    return state
