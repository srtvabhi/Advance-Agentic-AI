from models.state_models import RoutingState
from services.llm_service import ask_llm


async def technical_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a technical specialist. Focus on APIs, data, architecture, and implementation.",
        state["question"],
    )
    return {"answer": answer}

