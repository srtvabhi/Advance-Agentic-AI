from langsmith import traceable

from models.orchestration_models import OrchestrationState
from services.llm_service import ask_model
from services.retrieval_service import retrieve_policy_context
from services.tool_service import run_enterprise_tools


@traceable(name="rag_retrieval_node", run_type="retriever")
def rag_retrieval_node(state: OrchestrationState) -> OrchestrationState:
    # Retrieves policy context before agent planning.
    state["retrieved_context"] = retrieve_policy_context(state["user_request"])
    return state


@traceable(name="tool_execution_node", run_type="tool")
def tool_execution_node(state: OrchestrationState) -> OrchestrationState:
    # Executes deterministic enterprise tools.
    state["tool_results"] = run_enterprise_tools(state["user_request"])
    return state


@traceable(name="planner_agent_node", run_type="chain")
def planner_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Planner agent creates the execution plan.
    state["planner_output"] = ask_model(
        "You are the planner agent in a multi-agent enterprise workflow.",
        (
            "Create a plan using the user request, retrieved policy context, and tool results.\n\n"
            f"User request: {state['user_request']}\n\n"
            f"Policy context:\n{state['retrieved_context']}\n\n"
            f"Tool results:\n{state['tool_results']}"
        ),
    )
    return state


@traceable(name="executor_agent_node", run_type="chain")
def executor_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Executor agent turns the plan into concrete steps.
    state["executor_output"] = ask_model(
        "You are the executor agent. Convert plans into safe operational actions.",
        (
            "Execute this plan in simulation mode. Include what would happen next, "
            "which tickets or approvals are needed, and what should not be automated.\n\n"
            f"Plan:\n{state['planner_output']}"
        ),
    )
    return state


@traceable(name="reviewer_agent_node", run_type="chain")
def reviewer_agent_node(state: OrchestrationState) -> OrchestrationState:
    # Reviewer agent checks quality, safety, and compliance.
    state["reviewer_output"] = ask_model(
        "You are the reviewer agent for security, compliance, and quality.",
        (
            "Review this simulated execution. Check grounding, safety, approval handling, missing steps, "
            "and operational risk.\n\n"
            f"Execution:\n{state['executor_output']}"
        ),
    )
    return state


@traceable(name="final_answer_node", run_type="chain")
def final_answer_node(state: OrchestrationState) -> OrchestrationState:
    # Produces final answer from planner, executor, and reviewer outputs.
    state["final_answer"] = (
        "# Multi-Agent RAG And Tools Result\n\n"
        f"## Retrieved Context\n{state['retrieved_context']}\n\n"
        f"## Tool Results\n{state['tool_results']}\n\n"
        f"## Planner Agent\n{state['planner_output']}\n\n"
        f"## Executor Agent\n{state['executor_output']}\n\n"
        f"## Reviewer Agent\n{state['reviewer_output']}"
    )
    return state
