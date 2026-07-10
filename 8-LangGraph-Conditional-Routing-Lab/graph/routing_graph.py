from langgraph.graph import END, START, StateGraph

from models.state_models import RoutingState
from nodes.business_node import business_node
from nodes.final_node import final_node
from nodes.general_node import general_node
from nodes.risk_node import risk_node
from nodes.router_node import router_node
from nodes.technical_node import technical_node


def choose_route(state: RoutingState) -> str:
    return state["route"]


def build_graph():
    graph = StateGraph(RoutingState)

    graph.add_node("router", router_node)
    graph.add_node("business", business_node)
    graph.add_node("technical", technical_node)
    graph.add_node("risk", risk_node)
    graph.add_node("general", general_node)
    graph.add_node("final", final_node)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        choose_route,
        {
            "business": "business",
            "technical": "technical",
            "risk": "risk",
            "general": "general",
        },
    )

    graph.add_edge("business", "final")
    graph.add_edge("technical", "final")
    graph.add_edge("risk", "final")
    graph.add_edge("general", "final")
    graph.add_edge("final", END)

    return graph.compile()

