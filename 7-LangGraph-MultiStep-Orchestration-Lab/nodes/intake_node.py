from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 1: Understand the user problem and extract enterprise requirements.


async def intake_node(state: WorkflowState) -> WorkflowState:
    requirements = await ask_llm(
        "You are a business intake analyst.",
        f"Extract business requirements, users, systems, risks, and success metrics:\n{state['problem']}",
    )
    return {"requirements": requirements}

