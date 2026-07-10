from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from models.state_models import ResilientState
from nodes.approval_node import approval_node
from nodes.extract_node import extract_node
from nodes.final_node import final_node
from nodes.validate_node import validate_node
from nodes.vendor_node import vendor_node


def route_after_validation(state: ResilientState) -> str:
    if state["validation_status"] == "invalid":
        return "final"
    return "vendor"


def route_after_vendor_check(state: ResilientState) -> str:
    if state["vendor_status"] == "success":
        return "approval"
    if state.get("retry_count", 0) < 2:
        return "vendor"
    return "final"


def build_graph():
    graph = StateGraph(ResilientState)

    graph.add_node("extract", extract_node)
    graph.add_node("validate", validate_node)
    graph.add_node("vendor", vendor_node)
    graph.add_node("approval", approval_node)
    graph.add_node("final", final_node)

    graph.add_edge(START, "extract")
    graph.add_edge("extract", "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {"vendor": "vendor", "final": "final"},
    )
    graph.add_conditional_edges(
        "vendor",
        route_after_vendor_check,
        {"vendor": "vendor", "approval": "approval", "final": "final"},
    )
    graph.add_edge("approval", "final")
    graph.add_edge("final", END)

    return graph.compile(checkpointer=InMemorySaver())

