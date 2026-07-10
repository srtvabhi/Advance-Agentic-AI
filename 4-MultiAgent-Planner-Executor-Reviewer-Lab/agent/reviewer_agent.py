from agents import Agent

from config.settings import get_model_name


# Reviewer Agent: checks quality, risk, and missing details.


def create_reviewer_agent() -> Agent:
    return Agent(
        name="Reviewer Agent",
        model=get_model_name(),
        instructions=(
            "You are a reviewer agent. Review the plan and execution. "
            "Identify missing steps, risks, unclear ownership, and improvement suggestions."
        ),
    )

