from agents import Agent

from config.settings import get_model_name


# Planner Agent: creates a structured plan.


def create_planner_agent() -> Agent:
    return Agent(
        name="Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planner agent. Break the user goal into 4 to 6 clear steps. "
            "For each step include owner, action, and expected output. Do not execute."
        ),
    )

