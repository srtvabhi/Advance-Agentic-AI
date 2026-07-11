from langgraph.graph import END, StateGraph

from models.architecture_models import ArchitectureState
from nodes.architecture_nodes import architecture_node, cost_latency_node, deployment_node, intake_node, reliability_node, summary_node


def build_architecture_graph():
    graph = StateGraph(ArchitectureState)
    graph.add_node("intake", intake_node)
    graph.add_node("architecture", architecture_node)
    graph.add_node("deployment", deployment_node)
    graph.add_node("reliability", reliability_node)
    graph.add_node("cost_latency", cost_latency_node)
    graph.add_node("summary", summary_node)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "architecture")
    graph.add_edge("architecture", "deployment")
    graph.add_edge("deployment", "reliability")
    graph.add_edge("reliability", "cost_latency")
    graph.add_edge("cost_latency", "summary")
    graph.add_edge("summary", END)
    return graph.compile()
