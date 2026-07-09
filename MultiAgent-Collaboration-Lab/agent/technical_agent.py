from agents import Agent

from config.settings import get_model_name


def create_technical_agent() -> Agent:
    return Agent(
        name="Technical Agent",
        model=get_model_name(),
        instructions=(
            "You are a technical architecture agent. Identify systems, data, APIs, "
            "tools, orchestration approach, and integration points. Keep it concise."
        ),
    )

