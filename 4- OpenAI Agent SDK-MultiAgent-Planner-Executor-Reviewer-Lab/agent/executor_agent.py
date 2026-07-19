from agents import Agent

from config.settings import get_model_name
from tools.approval_tool import check_human_approval


# Executor Agent: turns the plan into practical actions.


def create_executor_agent() -> Agent:
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an executor agent. Convert the plan into practical execution actions. "
            "Use check_human_approval only when the prompt does not already contain a human approval decision. "
            "If the prompt says HUMAN_APPROVAL_DECISION: APPROVED, do not ask for approval again and do not call the approval tool again. "
            "In that case, continue by creating execution artifacts such as runbook steps, checklists, owners, validation steps, and audit evidence. "
            "If the prompt says HUMAN_APPROVAL_DECISION: DENIED, stop the workflow. "
            "Do not claim you actually changed production systems; this lab simulates execution planning."
        ),
        tools=[check_human_approval],
    )
