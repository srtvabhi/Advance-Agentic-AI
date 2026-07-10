from autogen_agentchat.agents import AssistantAgent

from tools.incident_tools import (
    check_service_health,
    create_incident_ticket,
    notify_response_team,
)


def create_operations_agent(model_client):
    return AssistantAgent(
        name="operations_agent",
        model_client=model_client,
        tools=[check_service_health, create_incident_ticket, notify_response_team],
        max_tool_iterations=3,
        system_message=(
            "You are an autonomous operations agent. Use your tools to check health, "
            "create an incident ticket, and notify the response team when the task describes an outage. "
            "Keep your final message under 8 short bullets."
        ),
    )


def create_root_cause_agent(model_client):
    return AssistantAgent(
        name="root_cause_agent",
        model_client=model_client,
        system_message=(
            "You are a root cause analyst. Review the operations findings and propose likely causes, "
            "mitigation steps, and validation checks. Keep your answer under 8 short bullets."
        ),
    )


def create_comms_agent(model_client):
    return AssistantAgent(
        name="communications_agent",
        model_client=model_client,
        system_message=(
            "You are a communications agent. Draft a short internal stakeholder update with status, "
            "impact, action owner, and next update time. Keep your answer under 8 short bullets."
        ),
    )


def create_manager_agent(model_client):
    return AssistantAgent(
        name="incident_manager",
        model_client=model_client,
        system_message=(
            "You are the incident manager. Summarize the autonomous ecosystem's final action plan. "
            "Include ticket, diagnosis, mitigation, communication, and next steps. Keep your answer under 10 short bullets."
        ),
    )
