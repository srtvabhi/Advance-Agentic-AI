from models.state_models import RoutingState
from services.llm_service import ask_llm


async def general_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a helpful general assistant. Answer simply and clearly.",
        state["question"],
    )
    return {"answer": answer}

