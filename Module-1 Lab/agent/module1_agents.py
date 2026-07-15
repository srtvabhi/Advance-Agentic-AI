from agents import Agent

from config.settings import get_model_name
from tools.approval import check_approval_required
from tools.calculator import calculate
from tools.datetime_tool import get_current_time
from tools.search import web_search
from tools.task_status import get_task_status
from tools.weather import get_weather


def create_enterprise_agent() -> Agent:
    """Create the main enterprise-grade tool-calling agent."""
    return Agent(
        name="Module 1 Enterprise Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful enterprise assistant. "
            "Use tools when the user asks about time, math, weather, or current web information. "
            "Keep answers clear and learner-friendly."
        ),
        tools=[get_current_time, calculate, get_weather, web_search],
    )


def create_stateful_agent() -> Agent:
    """Create an agent that can use prior conversation context."""
    return Agent(
        name="Module 1 Stateful Agent",
        model=get_model_name(),
        instructions=(
            "You are a stateful workflow assistant. "
            "Use the previous conversation messages to answer follow-up questions. "
            "Explain stateful agent concepts in simple language when helpful."
        ),
    )


def create_planner_agent() -> Agent:
    """Create the planning agent for the pipeline."""
    return Agent(
        name="Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planner. Break the user's enterprise problem into 5 clear steps. "
            "Do not execute the plan."
        ),
    )


def create_executor_agent() -> Agent:
    """Create the executor agent for the pipeline."""
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an executor. Convert the plan into practical actions with owners. "
            "Call check_approval_required for sensitive actions. "
            "Call get_task_status when task tracking is needed."
        ),
        tools=[check_approval_required, get_task_status],
    )


def create_reviewer_agent() -> Agent:
    """Create the reviewer agent for the pipeline."""
    return Agent(
        name="Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer. Check the execution output for risks, missing approvals, "
            "unclear ownership, and failure-handling gaps."
        ),
    )
