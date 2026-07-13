import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled


# Load only this folder's .env file and configure the OpenAI Agents SDK client.
def configure_agents_sdk() -> None:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    client = AsyncOpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


# Create a planner agent that breaks the task into steps.
def create_planner() -> Agent:
    return Agent(
        name="Planner",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Create a short step-by-step plan. Do not execute the plan.",
    )


# Create an executor agent that turns the plan into actions.
def create_executor() -> Agent:
    return Agent(
        name="Executor",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Convert the plan into practical actions with owners.",
    )


# Create a reviewer agent that checks the output.
def create_reviewer() -> Agent:
    return Agent(
        name="Reviewer",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="Review the workflow. Mention missing risks or approvals.",
    )


# Coordinate the agents sequentially: planner -> executor -> reviewer.
async def main() -> None:
    configure_agents_sdk()
    task = input("Enter enterprise task: ").strip() or "Create an employee onboarding workflow."

    plan = await Runner.run(create_planner(), task)
    execution = await Runner.run(create_executor(), plan.final_output)
    review = await Runner.run(create_reviewer(), execution.final_output)

    print("\n--- Planner ---\n", plan.final_output)
    print("\n--- Executor ---\n", execution.final_output)
    print("\n--- Reviewer ---\n", review.final_output)


if __name__ == "__main__":
    asyncio.run(main())


"""
Prompts :

Plan the migration of 50 applications to Azure within 6 months using a team of 10 engineers.

Create a project plan to reduce production incidents by 25% within 90 days.

"""
