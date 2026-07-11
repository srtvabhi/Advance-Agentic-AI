from typing import TypedDict


class ApprovalState(TypedDict):
    # Shared workflow state for approval-based AI execution.
    user_role: str
    requested_action: str
    risk_level: str
    approval_required: bool
    approval_reason: str
    approval_ticket: str
    execution_result: str
    audit_record: str
    final_output: str
