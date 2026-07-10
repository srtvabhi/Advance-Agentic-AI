from autogen_agentchat.agents import AssistantAgent


def create_policy_writer(model_client):
    return AssistantAgent(
        name="policy_writer",
        model_client=model_client,
        system_message=(
            "You are a policy writer. Draft a practical enterprise policy. "
            "Include purpose, scope, controls, approval workflow, audit evidence, and exception handling. "
            "Keep the draft concise and learner friendly."
        ),
    )


def create_validation_reviewer(model_client):
    return AssistantAgent(
        name="validation_reviewer",
        model_client=model_client,
        system_message=(
            "You are a validation reviewer. Review the policy against this checklist: "
            "purpose, scope, access control, human approval, logging, risk handling, owner, and audit evidence. "
            "Keep the review concise. End with either APPROVED or REVISION_REQUIRED."
        ),
    )
