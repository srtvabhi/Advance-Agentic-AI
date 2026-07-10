from agents import Agent

from config.settings import get_model_name


def create_coordinator_agent() -> Agent:
    return Agent(
        name="Coordinator Agent",
        model=get_model_name(),
        instructions=(
            "You are a coordinator agent. Combine outputs from business, technical, "
            "and risk agents into one clear final recommendation for enterprise leaders."
        ),
    )

