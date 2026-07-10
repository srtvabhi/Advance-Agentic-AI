import asyncio
import sys

from agent.business_agent import create_business_agent
from agent.general_agent import create_general_agent
from agent.risk_agent import create_risk_agent
from agent.router_agent import create_router_agent
from agent.technical_agent import create_technical_agent
from config.settings import configure_openai_client
from models.routing_models import RoutingDecision
from services.routing_service import normalize_route
from agents import Agent, Runner


# Lab 3: Dynamic Routing Between Multiple Agents
# Pattern: Supervisor/router orchestration.


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def select_agent(route: str, agents_by_route: dict[str, Agent]) -> Agent:
    return agents_by_route.get(route, agents_by_route["general"])


async def main() -> None:
    configure_openai_client()

    router_agent = create_router_agent()
    agents_by_route = {
        "business": create_business_agent(),
        "technical": create_technical_agent(),
        "risk": create_risk_agent(),
        "general": create_general_agent(),
    }

    print("Dynamic Agent Routing Lab")
    print("Ask a business, technical, risk, or general question.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        route_result = await Runner.run(router_agent, question)
        route = normalize_route(route_result.final_output)
        selected_agent = select_agent(route, agents_by_route)

        print(f"[Router selected: {route} -> {selected_agent.name}]")

        answer_result = await Runner.run(selected_agent, question)

        decision = RoutingDecision(
            question=question,
            route=route,
            selected_agent=selected_agent.name,
            answer=answer_result.final_output,
        )

        print("\n" + decision.to_text() + "\n")


if __name__ == "__main__":
    asyncio.run(main())
