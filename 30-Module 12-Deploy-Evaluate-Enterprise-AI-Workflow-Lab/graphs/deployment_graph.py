from langgraph.graph import END, StateGraph

from models.deployment_models import DeploymentEvaluationState
from nodes.deployment_nodes import cost_performance_node, deployment_plan_node, evaluation_plan_node, final_report_node, readiness_scorecard_node


def build_deployment_graph():
    # Builds the deployment and evaluation capstone workflow.
    graph = StateGraph(DeploymentEvaluationState)
    graph.add_node("deployment_plan", deployment_plan_node)
    graph.add_node("evaluation_plan", evaluation_plan_node)
    graph.add_node("readiness_scorecard", readiness_scorecard_node)
    graph.add_node("cost_performance", cost_performance_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("deployment_plan")
    graph.add_edge("deployment_plan", "evaluation_plan")
    graph.add_edge("evaluation_plan", "readiness_scorecard")
    graph.add_edge("readiness_scorecard", "cost_performance")
    graph.add_edge("cost_performance", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()
