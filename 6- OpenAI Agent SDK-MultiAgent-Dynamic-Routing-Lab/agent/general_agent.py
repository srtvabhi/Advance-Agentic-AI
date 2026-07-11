from agents import Agent

from config.settings import get_model_name


def create_general_agent() -> Agent:
    return Agent(
        name="General Specialist",
        model=get_model_name(),
        instructions="You answer general questions clearly and simply.",
    )

