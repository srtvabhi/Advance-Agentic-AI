from agents import Agent

from config.settings import get_model_name


def create_technical_agent() -> Agent:
    return Agent(
        name="Technical Specialist",
        model=get_model_name(),
        instructions="You answer architecture, integration, API, data, and implementation questions.",
    )

