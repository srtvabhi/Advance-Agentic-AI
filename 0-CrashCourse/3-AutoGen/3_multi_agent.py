import asyncio
import os
import sys
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Load only this folder's .env file and create an AutoGen OpenAI model client.
def create_model_client() -> OpenAIChatCompletionClient:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        model_info={"vision": False, "function_calling": True, "json_output": False, "family": "unknown", "structured_output": False},
    )


# Create three coordinating AutoGen agents.
def create_team(model_client) -> RoundRobinGroupChat:
    planner = AssistantAgent("planner", model_client=model_client, system_message="Create a short plan.")
    executor = AssistantAgent("executor", model_client=model_client, system_message="Turn the plan into action steps.")
    reviewer = AssistantAgent("reviewer", model_client=model_client, system_message="Review risks and missing approvals.")
    return RoundRobinGroupChat([planner, executor, reviewer], termination_condition=MaxMessageTermination(4))


# Run the AutoGen multi-agent group conversation.
async def main() -> None:
    model_client = create_model_client()
    team = create_team(model_client)
    task = input("Enter enterprise task: ").strip() or "Design a customer support automation workflow."
    try:
        result = await team.run(task=task)
        for message in result.messages:
            if type(message).__name__ == "ThoughtEvent":
                continue
            source = getattr(message, "source", "unknown")
            content = getattr(message, "content", "")
            if content:
                print(f"\n--- {source} ---\n{content}")
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())


"""
Prompts :

Plan the migration of 50 applications to Azure within 6 months using a team of 10 engineers.

Create a project plan to reduce production incidents by 25% within 90 days.

"""
