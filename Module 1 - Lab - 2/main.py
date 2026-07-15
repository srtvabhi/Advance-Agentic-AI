import asyncio
import sys

from agents import Runner

from agent.change_agents import (
    create_architecture_agent,
    create_executor_agent,
    create_intake_agent,
    create_planner_agent,
    create_reviewer_agent,
)
from config.settings import configure_openai_client
from memory.change_memory import ChangeConversationMemory
from models.change_models import ChangeRequest, PipelineResult


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_CHANGE = ChangeRequest(
    application="Customer Billing Portal",
    environment="Production",
    change_summary="Deploy a new invoice search API and migrate invoice index data",
    business_impact="Customers may be unable to search invoices during deployment if rollback fails",
)


def print_intro() -> None:
    """Show the lab scenario and objectives."""
    print("Module 1 - Lab 2: Enterprise Change Readiness Agent\n")
    print("Problem statement:")
    print("A team needs an AI assistant to prepare a production change request.")
    print("The assistant must remember change details, use enterprise tools, and build a rollout pipeline.\n")
    print("Objectives covered:")
    print("1. Design an enterprise-grade agent architecture")
    print("2. Build a stateful agent workflow design")
    print("3. Create an AI planning and execution pipeline\n")


async def collect_change_context(memory: ChangeConversationMemory) -> str:
    """Collect change request context using a stateful intake conversation."""
    intake_agent = create_intake_agent()
    print("Step 1: Stateful Change Intake")
    print("Tell the agent about the change. Press Enter to use the default change request.")
    print("Type 'done' when you are finished adding details.\n")

    first_message = input("Change detail: ").strip()
    if not first_message:
        first_message = DEFAULT_CHANGE.to_prompt()

    memory.add_user_message(first_message)
    result = await Runner.run(intake_agent, memory.get_items())
    memory.update_from_result(result)
    print("\nIntake Agent:", result.final_output, "\n")

    while True:
        message = input("Add detail or type done: ").strip()
        if message.lower() in {"done", "exit", "quit"}:
            break
        if not message:
            continue

        memory.add_user_message(message)
        result = await Runner.run(intake_agent, memory.get_items())
        memory.update_from_result(result)
        print("\nIntake Agent:", result.final_output, "\n")

    return memory.show_memory()


async def assess_enterprise_architecture(intake_summary: str) -> str:
    """Use enterprise tools to assess readiness of the change architecture."""
    architecture_agent = create_architecture_agent()
    prompt = f"""
Use the enterprise tools to assess this change request.

Change request context:
{intake_summary}

Assess risk, approval needs, maintenance window, and task tracking.
"""
    result = await Runner.run(architecture_agent, prompt)
    print("\n--- Step 2: Enterprise Architecture Readiness ---\n")
    print(result.final_output)
    return result.final_output


async def run_planning_pipeline(intake_summary: str, architecture_summary: str) -> PipelineResult:
    """Run planner, executor, and reviewer agents for the change request."""
    planner_agent = create_planner_agent()
    executor_agent = create_executor_agent()
    reviewer_agent = create_reviewer_agent()

    plan_prompt = f"""
Create a rollout plan for this enterprise change.

Change context:
{intake_summary}

Architecture readiness:
{architecture_summary}
"""
    plan_result = await Runner.run(planner_agent, plan_prompt)
    print("\n--- Step 3A: Planner Output ---\n")
    print(plan_result.final_output)

    execution_prompt = f"""
Convert this rollout plan into execution tasks.
Call approval and task tools where useful.

Change context:
{intake_summary}

Plan:
{plan_result.final_output}
"""
    execution_result = await Runner.run(executor_agent, execution_prompt)
    print("\n--- Step 3B: Executor Output ---\n")
    print(execution_result.final_output)

    review_prompt = f"""
Review this change pipeline for enterprise readiness.

Change context:
{intake_summary}

Architecture readiness:
{architecture_summary}

Plan:
{plan_result.final_output}

Execution:
{execution_result.final_output}
"""
    review_result = await Runner.run(reviewer_agent, review_prompt)
    print("\n--- Step 3C: Reviewer Output ---\n")
    print(review_result.final_output)

    return PipelineResult(
        intake_summary=intake_summary,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )


async def main() -> None:
    """Run the full Module 1 Lab 2 workflow."""
    configure_openai_client()
    memory = ChangeConversationMemory()

    print_intro()
    intake_summary = await collect_change_context(memory)
    architecture_summary = await assess_enterprise_architecture(intake_summary)
    pipeline_result = await run_planning_pipeline(intake_summary, architecture_summary)

    print("\n--- Final Module 1 Lab 2 Summary ---\n")
    print(pipeline_result.to_text())


if __name__ == "__main__":
    asyncio.run(main())
