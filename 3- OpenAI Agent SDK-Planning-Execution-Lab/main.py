import asyncio

from agent.executor_agent import create_executor_agent
from agent.planner_agent import create_planner_agent
from agent.reviewer_agent import create_reviewer_agent
from config.settings import configure_openai_client
from models.pipeline_models import PipelineResult
from agents import Runner


# Planning Execution Lab
# Objective: Create an AI planning and execution pipeline.
# Problem statement: Plan and execute an employee onboarding workflow.


DEFAULT_PROBLEM = (
    "Create an employee onboarding workflow for a new software engineer. "
    "Include HR setup, laptop provisioning, account access, team introduction, "
    "training plan, and manager review."
)


async def main() -> None:
    configure_openai_client()

    planner_agent = create_planner_agent()
    executor_agent = create_executor_agent()
    reviewer_agent = create_reviewer_agent()

    print("Planning Execution Lab is ready.\n")
    print("Default problem statement:")
    print(DEFAULT_PROBLEM)
    print()

    user_problem = input("Enter your problem statement, or press Enter to use default: ").strip()
    problem_statement = user_problem or DEFAULT_PROBLEM

    # Step 1: Planner creates the plan.
    plan_result = await Runner.run(planner_agent, problem_statement)
    print("\n--- Step 1: Planner Output ---\n")
    print(plan_result.final_output)

    # Step 2: Executor converts the plan into execution actions.
    execution_prompt = f"""
Problem statement:
{problem_statement}

Plan:
{plan_result.final_output}

Execute this plan at a high level.
Call tools when approval or task status is needed.
"""

    execution_result = await Runner.run(executor_agent, execution_prompt)
    print("\n--- Step 2: Executor Output ---\n")
    print(execution_result.final_output)

    # Step 3: Reviewer checks the plan and execution.
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
    print("\n--- Step 3: Reviewer Output ---\n")
    print(review_result.final_output)

    # Store the final pipeline result in a simple model.
    pipeline_result = PipelineResult(
        problem=problem_statement,
        plan=plan_result.final_output,
        execution=execution_result.final_output,
        review=review_result.final_output,
    )

    print("\n--- Final Pipeline Summary ---\n")
    print(pipeline_result.to_text())


if __name__ == "__main__":
    asyncio.run(main())

