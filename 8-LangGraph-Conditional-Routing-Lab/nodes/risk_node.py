from models.state_models import RoutingState
from services.llm_service import ask_llm


async def risk_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a risk specialist. Focus on security, privacy, compliance, and governance.",
        state["question"],
    )
    return {"answer": answer}

