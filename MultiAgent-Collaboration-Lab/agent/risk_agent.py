from agents import Agent

from config.settings import get_model_name


def create_risk_agent() -> Agent:
    return Agent(
        name="Risk Agent",
        model=get_model_name(),
        instructions=(
            "You are a risk and governance agent. Identify security, privacy, "
            "compliance, operational, and quality risks. Keep it concise."
        ),
    )

