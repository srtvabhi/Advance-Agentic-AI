from agents import Agent

from config.settings import get_model_name


def create_business_agent() -> Agent:
    return Agent(
        name="Business Specialist",
        model=get_model_name(),
        instructions="You answer business process, ROI, adoption, and stakeholder questions.",
    )

