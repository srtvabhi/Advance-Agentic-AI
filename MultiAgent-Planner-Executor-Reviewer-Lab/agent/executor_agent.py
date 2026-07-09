from agents import Agent

from config.settings import get_model_name
from tools.approval_tool import check_human_approval


# Executor Agent: turns the plan into practical actions.


def create_executor_agent() -> Agent:
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an executor agent. Convert the plan into practical execution actions. "
            "Use check_human_approval for risky actions like production, security, payroll, "
            "customer email, deletion, or access changes."
        ),
        tools=[check_human_approval],
    )

