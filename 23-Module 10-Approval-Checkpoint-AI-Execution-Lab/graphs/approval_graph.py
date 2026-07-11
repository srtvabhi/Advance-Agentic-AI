from langgraph.graph import END, StateGraph

from models.approval_models import ApprovalState
from nodes.approval_nodes import audit_node, approval_checkpoint_node, execution_node, final_node, risk_assessment_node, route_after_risk


def build_approval_graph():
    # Builds a LangGraph workflow with a human approval checkpoint.
    graph = StateGraph(ApprovalState)
    graph.add_node("risk_assessment", risk_assessment_node)
    graph.add_node("approval_checkpoint", approval_checkpoint_node)
    graph.add_node("execution", execution_node)
    graph.add_node("audit", audit_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("risk_assessment")
    graph.add_conditional_edges(
        "risk_assessment",
        route_after_risk,
        {
            "approval": "approval_checkpoint",
            "execute": "execution",
        },
    )
    graph.add_edge("approval_checkpoint", "audit")
    graph.add_edge("execution", "audit")
    graph.add_edge("audit", "final")
    graph.add_edge("final", END)
    return graph.compile()
