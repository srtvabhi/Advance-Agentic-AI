from agents import Agent

from config.settings import get_model_name


def create_business_agent() -> Agent:
    return Agent(
        name="Business Agent",
        model=get_model_name(),
        instructions=(
            "You are a business analyst agent. Identify business goals, users, "
            "success metrics, and adoption considerations. Keep it concise."
        ),
    )

