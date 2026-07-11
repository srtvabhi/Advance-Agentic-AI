from langgraph.graph import END, StateGraph

from models.rag_eval_models import RAGEvaluationState
from nodes.rag_eval_nodes import generate_answer_node, llm_as_judge_node, observability_report_node, retrieve_context_node


def build_rag_eval_graph():
    # Builds a LangGraph workflow for RAG response evaluation.
    graph = StateGraph(RAGEvaluationState)
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("generate_answer", generate_answer_node)
    graph.add_node("llm_as_judge", llm_as_judge_node)
    graph.add_node("observability_report", observability_report_node)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "generate_answer")
    graph.add_edge("generate_answer", "llm_as_judge")
    graph.add_edge("llm_as_judge", "observability_report")
    graph.add_edge("observability_report", END)
    return graph.compile()
