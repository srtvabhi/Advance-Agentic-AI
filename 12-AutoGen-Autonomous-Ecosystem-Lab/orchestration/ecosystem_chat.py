from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from agents.ecosystem_agents import (
    create_comms_agent,
    create_manager_agent,
    create_operations_agent,
    create_root_cause_agent,
)


def create_incident_ecosystem(model_client):
    return RoundRobinGroupChat(
        participants=[
            create_operations_agent(model_client),
            create_root_cause_agent(model_client),
            create_comms_agent(model_client),
            create_manager_agent(model_client),
        ],
        termination_condition=MaxMessageTermination(5),
    )

