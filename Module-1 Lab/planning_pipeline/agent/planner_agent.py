from agents import Agent

from config.settings import get_model_name


# Planner Agent
# Responsibility: Break the problem into clear execution steps.


def create_planner_agent() -> Agent:
    return Agent(
        name="Planner Agent",
        model=get_model_name(),
        instructions=(
            "You are a planning agent. "
            "Break the user problem into 5 to 7 practical steps. "
            "For each step, include goal, owner, and expected output. "
            "Do not execute the plan."
        ),
    )

