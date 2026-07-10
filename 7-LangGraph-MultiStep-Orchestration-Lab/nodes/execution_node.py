from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 3: Convert the plan into an execution design.


async def execution_node(state: WorkflowState) -> WorkflowState:
    execution = await ask_llm(
        "You are an enterprise workflow executor.",
        f"Explain how to execute this plan. Include tools, owners, and checkpoints:\n{state['plan']}",
    )
    return {"execution": execution}

