import asyncio
import sys

from agent.business_agent import create_business_agent
from agent.coordinator_agent import create_coordinator_agent
from agent.risk_agent import create_risk_agent
from agent.technical_agent import create_technical_agent
from config.settings import configure_openai_client
from models.collaboration_models import CollaborationResult
from agents import Runner


# Lab 2: Multi-Agent Collaboration Pipeline
# Pattern: Concurrent orchestration + coordinator.


DEFAULT_SCENARIO = "Design an AI agent system for an enterprise HR helpdesk."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    configure_openai_client()

    business_agent = create_business_agent()
    technical_agent = create_technical_agent()
    risk_agent = create_risk_agent()
    coordinator_agent = create_coordinator_agent()

    print("Multi-Agent Collaboration Lab\n")
    scenario = input(f"Enter scenario, or press Enter for default:\n{DEFAULT_SCENARIO}\n\nScenario: ").strip()
    scenario = scenario or DEFAULT_SCENARIO

    # Run specialist agents at the same time.
    business_task = Runner.run(business_agent, scenario)
    technical_task = Runner.run(technical_agent, scenario)
    risk_task = Runner.run(risk_agent, scenario)

    business_result, technical_result, risk_result = await asyncio.gather(
        business_task,
        technical_task,
        risk_task,
    )

    print("\n--- Business Agent Output ---\n")
    print(business_result.final_output)
    print("\n--- Technical Agent Output ---\n")
    print(technical_result.final_output)
    print("\n--- Risk Agent Output ---\n")
    print(risk_result.final_output)

    coordinator_prompt = f"""
Scenario:
{scenario}

Business analysis:
{business_result.final_output}

Technical analysis:
{technical_result.final_output}

Risk analysis:
{risk_result.final_output}

Create one final recommendation.
"""

    final_result = await Runner.run(coordinator_agent, coordinator_prompt)
    print("\n--- Coordinator Final Output ---\n")
    print(final_result.final_output)

    collaboration = CollaborationResult(
        scenario=scenario,
        business_view=business_result.final_output,
        technical_view=technical_result.final_output,
        risk_view=risk_result.final_output,
        final_summary=final_result.final_output,
    )

    print("\n--- Final Collaboration Summary ---\n")
    print(collaboration.to_text())


if __name__ == "__main__":
    asyncio.run(main())
