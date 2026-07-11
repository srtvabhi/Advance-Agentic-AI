from langgraph.graph import END, StateGraph

from models.pipeline_models import PipelineState
from nodes.pipeline_nodes import final_report_node, receive_events_node, routing_node, scaling_node, worker_pool_node


def build_pipeline_graph():
    # Builds a sequential LangGraph workflow for scalable queue-based orchestration.
    graph = StateGraph(PipelineState)
    graph.add_node("receive_events", receive_events_node)
    graph.add_node("routing", routing_node)
    graph.add_node("worker_pool", worker_pool_node)
    graph.add_node("scaling", scaling_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("receive_events")
    graph.add_edge("receive_events", "routing")
    graph.add_edge("routing", "worker_pool")
    graph.add_edge("worker_pool", "scaling")
    graph.add_edge("scaling", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()
