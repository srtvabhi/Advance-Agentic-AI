from langgraph.graph import END, START, StateGraph

from models.state_models import WorkflowState
from nodes.execution_node import execution_node
from nodes.intake_node import intake_node
from nodes.planning_node import planning_node
from nodes.summary_node import summary_node


def build_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("intake", intake_node)
    graph.add_node("planning", planning_node)
    graph.add_node("execution", execution_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "intake")
    graph.add_edge("intake", "planning")
    graph.add_edge("planning", "execution")
    graph.add_edge("execution", "summary")
    graph.add_edge("summary", END)

    return graph.compile()

