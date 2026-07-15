from agents import Agent

from config.settings import get_model_name
from tools.change_tools import (
    assess_change_risk,
    check_change_approval,
    create_change_task,
    recommend_maintenance_window,
)


def create_intake_agent() -> Agent:
    """Create a stateful intake agent for collecting change details."""
    return Agent(
        name="Change Intake Agent",
        model=get_model_name(),
        instructions=(
            "You are a change intake assistant. "
            "Help the user describe an enterprise production change request. "
            "Remember details from previous messages and ask for missing information briefly."
        ),
    )


def create_architecture_agent() -> Agent:
    """Create an enterprise architecture agent with change-management tools."""
    return Agent(
        name="Enterprise Change Architecture Agent",
        model=get_model_name(),
        instructions=(
            "You are an enterprise change architecture agent. "
            "Use tools to assess change risk, approval needs, maintenance window, and task tracking. "
            "Return a concise readiness summary."
        ),
        tools=[assess_change_risk, check_change_approval, recommend_maintenance_window, create_change_task],
    )


def create_planner_agent() -> Agent:
    """Create a planner agent for the change pipeline."""
    return Agent(
        name="Change Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planner. Create a 5-step enterprise change rollout plan. "
            "Include preparation, validation, deployment, rollback, and communication."
        ),
    )


def create_executor_agent() -> Agent:
    """Create an executor agent that turns the plan into actions."""
    return Agent(
        name="Change Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an executor. Convert the plan into actionable tasks with owners. "
            "Use approval and task tools when needed."
        ),
        tools=[check_change_approval, create_change_task],
    )


def create_reviewer_agent() -> Agent:
    """Create a reviewer agent for risk and governance checks."""
    return Agent(
        name="Change Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer. Check for missing approvals, rollback gaps, ownership gaps, "
            "customer risk, downtime risk, and failure-handling gaps."
        ),
    )
