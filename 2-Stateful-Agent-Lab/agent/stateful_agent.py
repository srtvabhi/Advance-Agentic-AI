from agents import Agent

from config.settings import get_model_name


# This file defines the stateful workflow agent.
# The memory is handled in Memory.py and passed to this agent from main.py.


def create_stateful_agent() -> Agent:
    return Agent(
        name="Stateful Workflow Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful stateful workflow assistant. "
            "Use the previous conversation messages to answer follow-up questions. "
            "Explain stateful agent concepts in simple language for learners. "
            "When asked, identify what information you remember from the conversation."
        ),
    )

