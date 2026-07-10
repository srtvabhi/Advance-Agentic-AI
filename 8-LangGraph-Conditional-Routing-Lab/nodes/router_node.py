from models.state_models import RoutingState
from services.llm_service import ask_llm
from services.routing_service import normalize_route


async def router_node(state: RoutingState) -> RoutingState:
    route_text = await ask_llm(
        "You are a router. Return only one word: business, technical, risk, or general.",
        state["question"],
    )
    return {"route": normalize_route(route_text)}

