from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from agents.team_agents import (
    create_architect_agent,
    create_business_agent,
    create_coordinator_agent,
    create_security_agent,
)


def create_group_chat(model_client):
    agents = [
        create_business_agent(model_client),
        create_architect_agent(model_client),
        create_security_agent(model_client),
        create_coordinator_agent(model_client),
    ]

    return RoundRobinGroupChat(
        participants=agents,
        termination_condition=MaxMessageTermination(5),
    )

