from typing import NotRequired, TypedDict


class SupportWorkflowState(TypedDict):
    ticket_id: str
    customer_id: str
    subject: str
    body: str
    channel: str
    validation_error: NotRequired[str]
    contains_pii: NotRequired[bool]
    redacted_body: NotRequired[str]
    intent: NotRequired[str]
    urgency: NotRequired[str]
    confidence: NotRequired[float]
    classification_reason: NotRequired[str]
    retrieved_documents: NotRequired[list[dict]]
    draft_response: NotRequired[str]
    policy_passed: NotRequired[bool]
    policy_reason: NotRequired[str]
    route: NotRequired[str]
    final_status: NotRequired[str]
    final_response: NotRequired[str]
    model_target: NotRequired[str]
    model_used: NotRequired[str]
    retry_count: NotRequired[int]
    fallback_activated: NotRequired[bool]
    model_failures: NotRequired[list[dict]]
    trace: NotRequired[list[dict]]
    errors: NotRequired[list[str]]
