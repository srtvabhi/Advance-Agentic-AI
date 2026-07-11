from langgraph.graph import END, StateGraph

from models.orchestration_models import OrchestrationState
from nodes.orchestration_nodes import (
    executor_agent_node,
    final_answer_node,
    planner_agent_node,
    rag_retrieval_node,
    reviewer_agent_node,
    tool_execution_node,
)


def build_orchestration_graph():
    # Builds a multi-agent workflow with RAG and tools.
    graph = StateGraph(OrchestrationState)
    graph.add_node("rag_retrieval", rag_retrieval_node)
    graph.add_node("tool_execution", tool_execution_node)
    graph.add_node("planner_agent", planner_agent_node)
    graph.add_node("executor_agent", executor_agent_node)
    graph.add_node("reviewer_agent", reviewer_agent_node)
    graph.add_node("final_answer", final_answer_node)

    graph.set_entry_point("rag_retrieval")
    graph.add_edge("rag_retrieval", "tool_execution")
    graph.add_edge("tool_execution", "planner_agent")
    graph.add_edge("planner_agent", "executor_agent")
    graph.add_edge("executor_agent", "reviewer_agent")
    graph.add_edge("reviewer_agent", "final_answer")
    graph.add_edge("final_answer", END)
    return graph.compile()
