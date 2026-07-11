from models.approval_models import ApprovalState
from services.approval_service import create_approval_ticket, evaluate_approval, execute_action
from services.llm_service import ask_model


def risk_assessment_node(state: ApprovalState) -> ApprovalState:
    # Checks role and action risk before execution.
    risk_level, approval_required, reason = evaluate_approval(
        state["user_role"],
        state["requested_action"],
    )
    state["risk_level"] = risk_level
    state["approval_required"] = approval_required
    state["approval_reason"] = reason
    return state


def route_after_risk(state: ApprovalState) -> str:
    # Sends high-risk actions to approval and low-risk actions to execution.
    if state["approval_required"]:
        return "approval"
    return "execute"


def approval_checkpoint_node(state: ApprovalState) -> ApprovalState:
    # Stops execution and creates a human approval ticket.
    state["approval_ticket"] = create_approval_ticket(
        state["user_role"],
        state["requested_action"],
        state["approval_reason"],
    )
    state["execution_result"] = "Execution paused until human approval is completed."
    return state


def execution_node(state: ApprovalState) -> ApprovalState:
    # Executes only when approval is not required.
    state["execution_result"] = execute_action(state["requested_action"])
    return state


def audit_node(state: ApprovalState) -> ApprovalState:
    # Creates an audit trail for governance and compliance review.
    state["audit_record"] = (
        f"Role: {state['user_role']}\n"
        f"Action: {state['requested_action']}\n"
        f"Risk: {state['risk_level']}\n"
        f"Approval required: {state['approval_required']}\n"
        f"Reason: {state['approval_reason']}"
    )
    return state


def final_node(state: ApprovalState) -> ApprovalState:
    # Explains the approval checkpoint result for participants.
    state["final_output"] = ask_model(
        "You are an AI governance trainer.",
        (
            "Explain this human approval checkpoint workflow in simple terms. "
            "Mention why the action was paused or executed.\n\n"
            f"Audit record:\n{state['audit_record']}\n\n"
            f"Approval ticket:\n{state['approval_ticket']}\n\n"
            f"Execution result:\n{state['execution_result']}"
        ),
    )
    return state
