from models.state_models import WorkflowState
from services.llm_service import ask_llm


# Node 2: Create a step-by-step orchestration plan.


async def planning_node(state: WorkflowState) -> WorkflowState:
    plan = await ask_llm(
        "You are a LangGraph workflow planner.",
        f"Create a 5-step graph workflow plan for these requirements:\n{state['requirements']}",
    )
    return {"plan": plan}

