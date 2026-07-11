from langgraph.graph import END, StateGraph

from models.resiliency_models import ResiliencyState
from nodes.resiliency_nodes import fallback_node, final_node, primary_node, route_after_primary


def build_resiliency_graph():
    # Builds a LangGraph workflow with conditional retry and fallback routing.
    graph = StateGraph(ResiliencyState)
    graph.add_node("primary", primary_node)
    graph.add_node("fallback", fallback_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("primary")
    graph.add_conditional_edges(
        "primary",
        route_after_primary,
        {
            "retry": "primary",
            "fallback": "fallback",
            "final": "final",
        },
    )
    graph.add_edge("fallback", "final")
    graph.add_edge("final", END)
    return graph.compile()
