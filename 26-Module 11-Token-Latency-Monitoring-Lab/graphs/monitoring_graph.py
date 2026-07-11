from langgraph.graph import END, StateGraph

from models.monitoring_models import MonitoringState
from nodes.monitoring_nodes import draft_response_node, final_report_node, review_response_node, telemetry_summary_node


def build_monitoring_graph():
    # Builds a LangGraph workflow that records token and latency telemetry.
    graph = StateGraph(MonitoringState)
    graph.add_node("draft_response", draft_response_node)
    graph.add_node("review_response", review_response_node)
    graph.add_node("telemetry_summary", telemetry_summary_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("draft_response")
    graph.add_edge("draft_response", "review_response")
    graph.add_edge("review_response", "telemetry_summary")
    graph.add_edge("telemetry_summary", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()
