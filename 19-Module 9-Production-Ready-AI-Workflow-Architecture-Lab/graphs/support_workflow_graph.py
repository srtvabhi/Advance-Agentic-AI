from typing import Literal

from langgraph.graph import END, START, StateGraph

from models.support_models import SupportWorkflowState
from nodes.support_nodes import (
    assess_risk,
    classify_ticket,
    finalize_auto_response,
    finalize_failure,
    generate_response,
    policy_check,
    prepare_human_review,
    protect_sensitive_data,
    retrieve_knowledge_node,
    validate_ticket,
)


def route_after_validation(state: SupportWorkflowState) -> Literal["protect_sensitive_data", "finalize_failure"]:
    return "finalize_failure" if state.get("route") == "failed" else "protect_sensitive_data"


def route_after_classification(state: SupportWorkflowState) -> Literal["assess_risk", "prepare_human_review"]:
    return "prepare_human_review" if state.get("route") == "human_review" else "assess_risk"


def route_after_risk(state: SupportWorkflowState) -> Literal["retrieve_knowledge", "prepare_human_review"]:
    return "prepare_human_review" if state.get("route") == "human_review" else "retrieve_knowledge"


def route_after_generation(state: SupportWorkflowState) -> Literal["policy_check", "prepare_human_review"]:
    return "prepare_human_review" if state.get("route") == "human_review" else "policy_check"


def route_after_policy(state: SupportWorkflowState) -> Literal["finalize_auto_response", "prepare_human_review"]:
    return "finalize_auto_response" if state.get("route") == "auto_response" else "prepare_human_review"


# Build the production-style customer support workflow.
def build_support_workflow_graph():
    graph = StateGraph(SupportWorkflowState)

    graph.add_node("validate_ticket", validate_ticket)
    graph.add_node("protect_sensitive_data", protect_sensitive_data)
    graph.add_node("classify_ticket", classify_ticket)
    graph.add_node("assess_risk", assess_risk)
    graph.add_node("retrieve_knowledge", retrieve_knowledge_node)
    graph.add_node("generate_response", generate_response)
    graph.add_node("policy_check", policy_check)
    graph.add_node("finalize_auto_response", finalize_auto_response)
    graph.add_node("prepare_human_review", prepare_human_review)
    graph.add_node("finalize_failure", finalize_failure)

    graph.add_edge(START, "validate_ticket")
    graph.add_conditional_edges("validate_ticket", route_after_validation)
    graph.add_edge("protect_sensitive_data", "classify_ticket")
    graph.add_conditional_edges("classify_ticket", route_after_classification)
    graph.add_conditional_edges("assess_risk", route_after_risk)
    graph.add_edge("retrieve_knowledge", "generate_response")
    graph.add_conditional_edges("generate_response", route_after_generation)
    graph.add_conditional_edges("policy_check", route_after_policy)
    graph.add_edge("finalize_auto_response", END)
    graph.add_edge("prepare_human_review", END)
    graph.add_edge("finalize_failure", END)

    return graph.compile()
