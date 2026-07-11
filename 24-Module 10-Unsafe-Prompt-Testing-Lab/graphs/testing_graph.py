from langgraph.graph import END, StateGraph

from models.testing_models import PromptTestState
from nodes.testing_nodes import final_report_node, improvement_plan_node, load_tests_node, run_tests_node


def build_testing_graph():
    # Builds a LangGraph workflow for unsafe prompt testing.
    graph = StateGraph(PromptTestState)
    graph.add_node("load_tests", load_tests_node)
    graph.add_node("run_tests", run_tests_node)
    graph.add_node("improvement_plan", improvement_plan_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("load_tests")
    graph.add_edge("load_tests", "run_tests")
    graph.add_edge("run_tests", "improvement_plan")
    graph.add_edge("improvement_plan", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()
