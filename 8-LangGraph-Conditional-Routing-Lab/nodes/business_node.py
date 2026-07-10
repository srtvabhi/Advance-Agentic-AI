from models.state_models import RoutingState
from services.llm_service import ask_llm


async def business_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a business specialist. Focus on business goals, ROI, users, and adoption.",
        state["question"],
    )
    return {"answer": answer}

