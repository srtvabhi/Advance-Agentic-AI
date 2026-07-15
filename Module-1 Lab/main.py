import asyncio
import sys

from agents import Runner

from agent.module1_agents import (
    create_enterprise_agent,
    create_executor_agent,
    create_planner_agent,
    create_reviewer_agent,
    create_stateful_agent,
)
from config.settings import configure_openai_client
from memory.conversation_memory import ConversationMemory
from models.pipeline_models import PipelineResult


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_PROBLEM = (
    "Create an employee onboarding workflow for a new software engineer. "
    "Include HR setup, laptop provisioning, account access, team introduction, "
    "training plan, and manager review."
)


def show_menu() -> None:
    """Display the three Module 1 objectives."""
    print("Module-1 Lab: Advanced Agentic AI Architecture Patterns\n")
    print("1. Design an enterprise-grade agent architecture")
    print("2. Build a stateful agent workflow design")
    print("3. Create an AI planning and execution pipeline")
    print("q. Quit")


async def run_enterprise_architecture() -> None:
    """Run the enterprise-grade tool-calling agent objective."""
    agent = create_enterprise_agent()

    print("\nEnterprise Architecture Objective")
    print("Ask about time, math, weather, or web search.")
    print("Type 'back' to return to the main menu.\n")

    while True:
        question = input("Enterprise question: ").strip()
        if question.lower() in {"back", "exit", "quit"}:
            break
        if not question:
            continue

        result = await Runner.run(agent, question)
        print("\nAgent:", result.final_output, "\n")


async def run_stateful_workflow() -> None:
    """Run the stateful conversation workflow objective."""
    agent = create_stateful_agent()
    memory = ConversationMemory()

    print("\nStateful Workflow Objective")
    print("The agent remembers earlier messages during this running session.")
    print("Type 'memory' to inspect memory, 'clear' to clear memory, or 'back' for menu.\n")

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"back", "exit", "quit"}:
            break
        if user_message.lower() == "memory":
            print("\nStored Memory:\n" + memory.show_memory() + "\n")
            continue
        if user_message.lower() == "clear":
            memory.clear()
            print("\nMemory cleared.\n")
            continue
        if not user_message:
            continue

        memory.add_user_message(user_message)
        result = await Runner.run(agent, memory.get_items())
        print("\nAgent:", result.final_output, "\n")
        memory.update_from_result(result)


async def run_planning_pipeline() -> None:
    """Run the planner-executor-reviewer pipeline objective."""
    planner_agent = create_planner_agent()
    executor_agent = create_executor_agent()
    reviewer_agent = create_reviewer_agent()

    print("\nPlanning And Execution Pipeline Objective")
    print("Default problem:")
    print(DEFAULT_PROBLEM)
    print()

    user_problem = input("Enter problem statement, or press Enter for default: ").strip()
    problem_statement = user_problem or DEFAULT_PROBLEM

    plan_result = await Runner.run(planner_agent, problem_statement)
    print("\n--- Planner Output ---\n")
    print(plan_result.final_output)

    execution_prompt = f"""
Problem statement:
{problem_statement}

Plan:
{plan_result.final_output}

Execute this plan at a high level.
Call tools when approval checks or task tracking are needed.
"""
    execution_result = await Runner.run(executor_agent, execution_prompt)
    print("\n--- Executor Output ---\n")
    print(execution_result.final_output)

    review_prompt = f"""
Problem statement:
{problem_statement}

Planner output:
{plan_result.final_output}

Executor output:
{execution_result.final_output}

Review the pipeline and suggest improvements.
"""
    review_result = await Runner.run(reviewer_agent, review_prompt)
    print("\n--- Reviewer Output ---\n")
    print(review_result.final_output)

    pipeline_result = PipelineResult(
        problem=problem_statement,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )

    print("\n--- Final Pipeline Summary ---\n")
    print(pipeline_result.to_text())


async def main() -> None:
    """Configure the SDK and run the Module 1 menu."""
    configure_openai_client()

    while True:
        show_menu()
        choice = input("\nSelect objective: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("Goodbye.")
            break
        if choice == "1":
            await run_enterprise_architecture()
        elif choice == "2":
            await run_stateful_workflow()
        elif choice == "3":
            await run_planning_pipeline()
        else:
            print("Invalid choice. Select 1, 2, 3, or q.\n")


if __name__ == "__main__":
    asyncio.run(main())
