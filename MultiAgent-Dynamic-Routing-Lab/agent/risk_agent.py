from agents import Agent

from config.settings import get_model_name


def create_risk_agent() -> Agent:
    return Agent(
        name="Risk Specialist",
        model=get_model_name(),
        instructions="You answer security, compliance, privacy, safety, and governance questions.",
    )

