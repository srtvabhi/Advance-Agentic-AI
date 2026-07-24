from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

from models.procurement_models import ProcurementState
from nodes.procurement_nodes import (
    content_filter_guardrail,
    determine_approval_requirement,
    finalize_access_denied,
    finalize_invalid_request,
    finalize_recommendation,
    finalize_rejection,
    finalize_security_review,
    generate_grounded_assessment,
    human_approval_checkpoint,
    output_guardrail,
    privacy_guardrail,
    prompt_injection_guardrail,
    rbac_guardrail,
    retrieve_policies,
    validate_request,
)


# Route after request validation.
def route_after_validation(state: ProcurementState) -> str:
    return "finalize_invalid_request" if state.get("route") == "blocked" else "privacy_guardrail"


# Route after prompt injection scan.
def route_after_injection(state: ProcurementState) -> str:
    return "finalize_security_review" if state.get("route") == "security_review" else "content_filter_guardrail"


# Route after content filtering.
def route_after_content_filter(state: ProcurementState) -> str:
    return "finalize_security_review" if state.get("route") == "security_review" else "rbac_guardrail"


# Route after RBAC check.
def route_after_rbac(state: ProcurementState) -> str:
    return "retrieve_policies" if state.get("rbac_allowed") else "finalize_access_denied"


# Route after approved policy retrieval.
def route_after_retrieval(state: ProcurementState) -> str:
    return "finalize_security_review" if state.get("route") == "security_review" else "generate_grounded_assessment"


# Route after risk assessment generation.
def route_after_assessment(state: ProcurementState) -> str:
    return "finalize_security_review" if state.get("route") == "security_review" else "output_guardrail"


# Route after output guardrail verification.
def route_after_output_guardrail(state: ProcurementState) -> str:
    return "determine_approval_requirement" if state.get("output_guardrail_passed") else "finalize_security_review"


# Route to human approval only when policy requires it.
def route_after_approval_requirement(state: ProcurementState) -> str:
    return "human_approval_checkpoint" if state.get("approval_required") else "finalize_recommendation"


# Route after the graph resumes from human approval.
def route_after_human_decision(state: ProcurementState) -> str:
    decision = state.get("approval_decision", "escalate")
    if decision == "approve":
        return "finalize_recommendation"
    if decision == "reject":
        return "finalize_rejection"
    return "finalize_security_review"


# Build and compile the secure procurement workflow.
def build_procurement_graph():
    infrastructure_retry = RetryPolicy(
        initial_interval=1.0,
        backoff_factor=2.0,
        max_interval=8.0,
        max_attempts=3,
        jitter=True,
    )

    graph = StateGraph(ProcurementState)

    graph.add_node("validate_request", validate_request)
    graph.add_node("privacy_guardrail", privacy_guardrail)
    graph.add_node("prompt_injection_guardrail", prompt_injection_guardrail)
    graph.add_node("content_filter_guardrail", content_filter_guardrail)
    graph.add_node("rbac_guardrail", rbac_guardrail)
    graph.add_node("retrieve_policies", retrieve_policies, retry_policy=infrastructure_retry)
    graph.add_node("generate_grounded_assessment", generate_grounded_assessment, retry_policy=infrastructure_retry)
    graph.add_node("output_guardrail", output_guardrail)
    graph.add_node("determine_approval_requirement", determine_approval_requirement)
    graph.add_node("human_approval_checkpoint", human_approval_checkpoint)
    graph.add_node("finalize_recommendation", finalize_recommendation)
    graph.add_node("finalize_rejection", finalize_rejection)
    graph.add_node("finalize_security_review", finalize_security_review)
    graph.add_node("finalize_access_denied", finalize_access_denied)
    graph.add_node("finalize_invalid_request", finalize_invalid_request)

    graph.add_edge(START, "validate_request")
    graph.add_conditional_edges("validate_request", route_after_validation)
    graph.add_edge("privacy_guardrail", "prompt_injection_guardrail")
    graph.add_conditional_edges("prompt_injection_guardrail", route_after_injection)
    graph.add_conditional_edges("content_filter_guardrail", route_after_content_filter)
    graph.add_conditional_edges("rbac_guardrail", route_after_rbac)
    graph.add_conditional_edges("retrieve_policies", route_after_retrieval)
    graph.add_conditional_edges("generate_grounded_assessment", route_after_assessment)
    graph.add_conditional_edges("output_guardrail", route_after_output_guardrail)
    graph.add_conditional_edges("determine_approval_requirement", route_after_approval_requirement)
    graph.add_conditional_edges("human_approval_checkpoint", route_after_human_decision)

    for terminal_node in [
        "finalize_recommendation",
        "finalize_rejection",
        "finalize_security_review",
        "finalize_access_denied",
        "finalize_invalid_request",
    ]:
        graph.add_edge(terminal_node, END)

    return graph.compile(checkpointer=InMemorySaver())
