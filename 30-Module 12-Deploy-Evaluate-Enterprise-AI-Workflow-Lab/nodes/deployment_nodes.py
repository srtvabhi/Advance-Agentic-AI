from langsmith import traceable

from models.deployment_models import DeploymentEvaluationState
from services.llm_service import ask_model
from services.readiness_service import calculate_readiness_score


@traceable(name="deployment_plan_node", run_type="chain")
def deployment_plan_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates Azure deployment planning guidance.
    state["deployment_plan"] = ask_model(
        "You are an Azure enterprise AI deployment architect.",
        (
            "Create an Azure deployment plan. Include environments, identity, networking, containers, "
            "model endpoint, queues, scaling, secrets, CI/CD, and rollback.\n\n"
            f"Workflow description:\n{state['workflow_description']}"
        ),
    )
    return state


@traceable(name="evaluation_plan_node", run_type="chain")
def evaluation_plan_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates quality, safety, and operational evaluation guidance.
    state["evaluation_plan"] = ask_model(
        "You are an enterprise AI evaluator.",
        (
            "Create an evaluation plan for this enterprise AI workflow. Include functional tests, RAG quality, "
            "tool correctness, safety tests, latency, token cost, LangSmith traces, and human review.\n\n"
            f"Workflow:\n{state['workflow_description']}\n\nDeployment:\n{state['deployment_plan']}"
        ),
    )
    return state


@traceable(name="readiness_scorecard_node", run_type="chain")
def readiness_scorecard_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Calculates a deterministic readiness scorecard.
    state["readiness_scorecard"] = calculate_readiness_score(state["workflow_description"])
    return state


@traceable(name="cost_performance_node", run_type="chain")
def cost_performance_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Adds cost and performance optimization guidance.
    state["cost_performance_plan"] = ask_model(
        "You are a cost and performance optimization reviewer for production AI.",
        (
            "Create cost and performance guidance. Include token budgets, caching, batching, model routing, "
            "rate limits, autoscaling, and monitoring dashboards.\n\n"
            f"Deployment plan:\n{state['deployment_plan']}\n\n"
            f"Evaluation plan:\n{state['evaluation_plan']}\n\n"
            f"Scorecard:\n{state['readiness_scorecard']}"
        ),
    )
    return state


@traceable(name="final_report_node", run_type="chain")
def final_report_node(state: DeploymentEvaluationState) -> DeploymentEvaluationState:
    # Creates the final deployment and evaluation report.
    state["final_report"] = (
        "# Deployment And Evaluation Report\n\n"
        f"## Deployment Plan\n{state['deployment_plan']}\n\n"
        f"## Evaluation Plan\n{state['evaluation_plan']}\n\n"
        f"## Readiness Scorecard\n{state['readiness_scorecard']}\n\n"
        f"## Cost And Performance Plan\n{state['cost_performance_plan']}"
    )
    return state
