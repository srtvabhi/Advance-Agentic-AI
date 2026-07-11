from agents import Agent

from config.settings import get_model_name


# Reviewer Agent
# Responsibility: Review the plan and execution for quality and risk.


def create_reviewer_agent() -> Agent:
    return Agent(
        name="Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer agent. "
            "Review the planner and executor outputs. "
            "Check for missing steps, unclear ownership, approval gaps, "
            "failure handling, and business risks. "
            "Return a short review with improvements."
        ),
    )

