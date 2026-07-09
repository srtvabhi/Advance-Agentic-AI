from agents import Agent

from config.settings import get_model_name
from tools.approval_tool import check_approval_required
from tools.task_tool import get_task_status


# Executor Agent
# Responsibility: Convert the plan into practical execution actions.
# It can call tools for approval checks and task status.


def create_executor_agent() -> Agent:
    return Agent(
        name="Executor Agent",
        model=get_model_name(),
        instructions=(
            "You are an execution agent. "
            "Convert the plan into clear actions. "
            "Call check_approval_required for actions that may need human approval. "
            "Call get_task_status when you mention task tracking or progress. "
            "Keep the execution easy for learners to understand."
        ),
        tools=[check_approval_required, get_task_status],
    )

