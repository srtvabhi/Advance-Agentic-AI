from models.guardrail_models import GuardrailState
from services.guardrail_service import build_safe_prompt, classify_request
from services.llm_service import ask_model


def input_guardrail_node(state: GuardrailState) -> GuardrailState:
    # Classifies the request before the model sees it.
    classification, reason = classify_request(state["user_request"])
    state["classification"] = classification
    state["risk_reason"] = reason
    state["safe_prompt"] = build_safe_prompt(state["user_request"])
    return state


def route_after_guardrail(state: GuardrailState) -> str:
    # Routes safe requests to the LLM and unsafe requests to a refusal response.
    if state["classification"] == "blocked":
        return "blocked"
    if state["classification"] == "needs_review":
        return "review"
    return "safe"


def safe_agent_node(state: GuardrailState) -> GuardrailState:
    # Calls the LLM only after the request passes the guardrail checks.
    state["agent_answer"] = ask_model(
        "You are a secure enterprise AI assistant. Be helpful, concise, and safety-aware.",
        state["safe_prompt"],
    )
    return state


def blocked_response_node(state: GuardrailState) -> GuardrailState:
    # Produces a controlled refusal without sending the unsafe request to the model.
    state["agent_answer"] = (
        "Request blocked by guardrails. The request appears to ask for unsafe, private, "
        "or instruction-bypassing behavior."
    )
    return state


def review_response_node(state: GuardrailState) -> GuardrailState:
    # Produces a human-review response for ambiguous requests.
    state["agent_answer"] = "Request requires human review before the AI agent can continue."
    return state


def audit_node(state: GuardrailState) -> GuardrailState:
    # Creates a traceable audit record for governance review.
    state["audit_record"] = (
        f"Classification: {state['classification']}\n"
        f"Reason: {state['risk_reason']}\n"
        f"Final action: {state['agent_answer'][:160]}"
    )
    return state


def final_node(state: GuardrailState) -> GuardrailState:
    # Creates a learner-friendly final explanation of the guardrail decision.
    if state["classification"] != "safe":
        state["final_output"] = (
            "The guardrail workflow stopped this request before model execution. "
            f"Classification: {state['classification']}. "
            "The request was not forwarded to the LLM because it matched enterprise safety rules. "
            "An audit record was created so security, compliance, or a human reviewer can inspect the decision."
        )
        return state

    request_summary = "Safe request" if state["classification"] == "safe" else "Unsafe request content removed from model-facing summary"
    state["final_output"] = ask_model(
        "You are a responsible AI trainer.",
        (
            "Explain this guardrail workflow result in simple terms for workshop participants.\n\n"
            f"Request summary: {request_summary}\n"
            f"Classification: {state['classification']}\n"
            f"Reason: {state['risk_reason']}\n"
            f"Agent answer: {state['agent_answer']}\n"
            f"Audit record: {state['audit_record']}"
        ),
    )
    return state
