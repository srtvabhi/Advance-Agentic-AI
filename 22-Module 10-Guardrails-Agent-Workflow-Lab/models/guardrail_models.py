from typing import TypedDict


class GuardrailState(TypedDict):
    # Shared workflow state for the guardrail graph.
    user_request: str
    classification: str
    risk_reason: str
    safe_prompt: str
    agent_answer: str
    audit_record: str
    final_output: str
