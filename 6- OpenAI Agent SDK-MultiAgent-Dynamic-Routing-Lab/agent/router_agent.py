from agents import Agent

from config.settings import get_model_name


def create_router_agent() -> Agent:
    return Agent(
        name="Supervisor Router Agent",
        model=get_model_name(),
        instructions=(
            "You are a supervisor router agent. Route the user question to the best specialist. "
            "Reply with only one route word: business, technical, risk, or general."
        ),
    )

