from autogen_agentchat.agents import AssistantAgent


def create_business_agent(model_client):
    return AssistantAgent(
        name="business_analyst",
        model_client=model_client,
        system_message=(
            "You are a business analyst. Explain business goals, users, value, "
            "success metrics, and adoption risks. Keep your answer under 8 short bullets."
        ),
    )


def create_architect_agent(model_client):
    return AssistantAgent(
        name="solution_architect",
        model_client=model_client,
        system_message=(
            "You are a solution architect. Explain systems, APIs, data flow, "
            "agent responsibilities, and integration points. Keep your answer under 8 short bullets."
        ),
    )


def create_security_agent(model_client):
    return AssistantAgent(
        name="security_reviewer",
        model_client=model_client,
        system_message=(
            "You are a security reviewer. Explain privacy, compliance, access control, "
            "audit logging, and governance risks. Keep your answer under 8 short bullets."
        ),
    )


def create_coordinator_agent(model_client):
    return AssistantAgent(
        name="coordinator",
        model_client=model_client,
        system_message=(
            "You are the coordinator. Combine the other agents' ideas into one final "
            "enterprise recommendation with clear next steps. Keep your answer under 10 short bullets."
        ),
    )
