from typing import Any, Literal

from typing_extensions import NotRequired, TypedDict


Role = Literal[
    "employee",
    "procurement_analyst",
    "procurement_manager",
    "compliance_officer",
]


# Shared LangGraph state. Each node reads and writes a small part of this state.
class ProcurementState(TypedDict):
    request_id: str
    requester_id: str
    requester_role: Role
    requested_action: str
    vendor_name: str
    proposal_text: str
    purchase_amount_usd: float
    data_classification: str

    validation_errors: NotRequired[list[str]]
    pii_types: NotRequired[list[str]]
    redacted_proposal: NotRequired[str]
    injection_detected: NotRequired[bool]
    injection_signals: NotRequired[list[str]]
    content_categories: NotRequired[list[str]]
    rbac_allowed: NotRequired[bool]

    retrieved_policies: NotRequired[list[dict[str, Any]]]
    assessment: NotRequired[dict[str, Any]]
    grounded: NotRequired[bool]
    unsupported_claims: NotRequired[list[str]]
    output_guardrail_passed: NotRequired[bool]

    approval_required: NotRequired[bool]
    required_approver_role: NotRequired[str]
    approval_decision: NotRequired[str]
    approver_id: NotRequired[str]
    approver_role: NotRequired[str]
    approval_comment: NotRequired[str]

    route: NotRequired[str]
    final_status: NotRequired[str]
    final_recommendation: NotRequired[str]

    audit_log: NotRequired[list[dict[str, Any]]]
    errors: NotRequired[list[str]]
