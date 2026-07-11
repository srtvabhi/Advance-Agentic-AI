from langgraph.graph import END, StateGraph

from models.guardrail_models import GuardrailState
from nodes.guardrail_nodes import (
    audit_node,
    blocked_response_node,
    final_node,
    input_guardrail_node,
    review_response_node,
    route_after_guardrail,
    safe_agent_node,
)


def build_guardrail_graph():
    # Builds a LangGraph workflow with pre-model guardrails and auditability.
    graph = StateGraph(GuardrailState)
    graph.add_node("input_guardrail", input_guardrail_node)
    graph.add_node("safe_agent", safe_agent_node)
    graph.add_node("blocked_response", blocked_response_node)
    graph.add_node("review_response", review_response_node)
    graph.add_node("audit", audit_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("input_guardrail")
    graph.add_conditional_edges(
        "input_guardrail",
        route_after_guardrail,
        {
            "safe": "safe_agent",
            "blocked": "blocked_response",
            "review": "review_response",
        },
    )
    graph.add_edge("safe_agent", "audit")
    graph.add_edge("blocked_response", "audit")
    graph.add_edge("review_response", "audit")
    graph.add_edge("audit", "final")
    graph.add_edge("final", END)
    return graph.compile()
