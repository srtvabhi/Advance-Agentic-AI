import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments


# Load only this folder's .env file and create a Semantic Kernel instance.
def create_kernel() -> Kernel:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    kernel = Kernel()
    client = AsyncOpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])
    kernel.add_service(OpenAIChatCompletion(ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"], async_client=client, service_id="foundry-chat"))
    return kernel


# Semantic agent: planner creates a plan.
async def planner_agent(kernel: Kernel, task: str) -> str:
    result = await kernel.invoke_prompt("You are a planner. Create 5 short steps for:\n{{$task}}", arguments=KernelArguments(task=task))
    return str(result)


# Semantic agent: executor adds owners and actions.
async def executor_agent(kernel: Kernel, plan: str) -> str:
    result = await kernel.invoke_prompt("You are an executor. Add owners and actions to this plan:\n{{$plan}}", arguments=KernelArguments(plan=plan))
    return str(result)


# Semantic agent: reviewer checks risks and approvals.
async def reviewer_agent(kernel: Kernel, execution: str) -> str:
    result = await kernel.invoke_prompt("You are a reviewer. Identify risks and missing approvals:\n{{$execution}}", arguments=KernelArguments(execution=execution))
    return str(result)


# Coordinate three Semantic Kernel prompt agents.
async def main() -> None:
    kernel = create_kernel()
    task = input("Enter enterprise task: ").strip() or "Create a vendor onboarding workflow."
    plan = await planner_agent(kernel, task)
    execution = await executor_agent(kernel, plan)
    review = await reviewer_agent(kernel, execution)

    print("\n--- Planner ---\n", plan)
    print("\n--- Executor ---\n", execution)
    print("\n--- Reviewer ---\n", review)


if __name__ == "__main__":
    asyncio.run(main())

