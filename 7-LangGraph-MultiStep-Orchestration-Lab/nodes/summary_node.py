from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 4: Summarize the final workflow for leaders and engineers.


async def summary_node(state: WorkflowState) -> WorkflowState:
    summary = await ask_llm(
        "You are a solution architect.",
        (
            "Create a concise final summary for this LangGraph workflow.\n\n"
            f"Requirements:\n{state['requirements']}\n\n"
            f"Plan:\n{state['plan']}\n\n"
            f"Execution:\n{state['execution']}"
        ),
    )
    return {"summary": summary}

