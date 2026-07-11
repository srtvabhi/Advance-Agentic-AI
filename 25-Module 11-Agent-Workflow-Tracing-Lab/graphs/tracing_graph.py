from langgraph.graph import END, StateGraph

from models.tracing_models import TracingState
from nodes.tracing_nodes import final_report_node, investigation_node, resolution_node, trace_notes_node, triage_node


def build_tracing_graph():
    # Builds a traceable multi-step LangGraph workflow.
    graph = StateGraph(TracingState)
    graph.add_node("triage", triage_node)
    graph.add_node("investigation", investigation_node)
    graph.add_node("resolution", resolution_node)
    graph.add_node("trace_notes", trace_notes_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("triage")
    graph.add_edge("triage", "investigation")
    graph.add_edge("investigation", "resolution")
    graph.add_edge("resolution", "trace_notes")
    graph.add_edge("trace_notes", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()
