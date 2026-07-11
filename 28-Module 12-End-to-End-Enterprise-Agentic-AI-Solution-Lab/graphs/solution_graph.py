from langgraph.graph import END, StateGraph

from models.solution_models import EnterpriseSolutionState
from nodes.solution_nodes import (
    architecture_node,
    final_solution_node,
    observability_governance_node,
    production_readiness_node,
    requirements_node,
    security_compliance_node,
)


def build_solution_graph():
    # Builds the end-to-end capstone solution graph.
    graph = StateGraph(EnterpriseSolutionState)
    graph.add_node("requirements", requirements_node)
    graph.add_node("architecture", architecture_node)
    graph.add_node("security_compliance", security_compliance_node)
    graph.add_node("observability_governance", observability_governance_node)
    graph.add_node("production_readiness", production_readiness_node)
    graph.add_node("final_solution", final_solution_node)

    graph.set_entry_point("requirements")
    graph.add_edge("requirements", "architecture")
    graph.add_edge("architecture", "security_compliance")
    graph.add_edge("security_compliance", "observability_governance")
    graph.add_edge("observability_governance", "production_readiness")
    graph.add_edge("production_readiness", "final_solution")
    graph.add_edge("final_solution", END)
    return graph.compile()
