from models.state_models import RoutingState


async def final_node(state: RoutingState) -> RoutingState:
    return {
        "final_response": (
            f"Route selected: {state['route']}\n\n"
            f"Answer:\n{state['answer']}"
        )
    }

