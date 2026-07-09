import asyncio
import sys

from agent.executor_agent import create_executor_agent
from agent.planner_agent import create_planner_agent
from agent.reviewer_agent import create_reviewer_agent
from config.settings import configure_openai_client
from models.workflow_models import WorkflowResult
from agents import Runner


# Lab 1: Planner-Executor-Reviewer Workflow
# Pattern: Sequential orchestration.


DEFAULT_GOAL = "Launch a customer support chatbot for an ecommerce company."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    configure_openai_client()

    planner = create_planner_agent()
    executor = create_executor_agent()
    reviewer = create_reviewer_agent()

    print("Planner-Executor-Reviewer Lab\n")
    goal = input(f"Enter goal, or press Enter for default:\n{DEFAULT_GOAL}\n\nGoal: ").strip()
    goal = goal or DEFAULT_GOAL

    plan_result = await Runner.run(planner, goal)
    print("\n--- Planner Output ---\n")
    print(plan_result.final_output)

    execution_prompt = f"Goal:\n{goal}\n\nPlan:\n{plan_result.final_output}\n\nExecute this plan."
    execution_result = await Runner.run(executor, execution_prompt)
    print("\n--- Executor Output ---\n")
    print(execution_result.final_output)

    review_prompt = (
        f"Goal:\n{goal}\n\nPlan:\n{plan_result.final_output}\n\n"
        f"Execution:\n{execution_result.final_output}\n\nReview this workflow."
    )
    review_result = await Runner.run(reviewer, review_prompt)
    print("\n--- Reviewer Output ---\n")
    print(review_result.final_output)

    final_result = WorkflowResult(
        goal=goal,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )

    print("\n--- Final Summary ---\n")
    print(final_result.to_text())


if __name__ == "__main__":
    asyncio.run(main())
