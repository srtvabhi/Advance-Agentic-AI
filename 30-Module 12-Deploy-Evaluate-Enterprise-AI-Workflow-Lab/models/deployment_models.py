from typing import TypedDict


class DeploymentEvaluationState(TypedDict):
    # Shared state for deployment and evaluation workflow.
    workflow_description: str
    deployment_plan: str
    evaluation_plan: str
    readiness_scorecard: str
    cost_performance_plan: str
    final_report: str
