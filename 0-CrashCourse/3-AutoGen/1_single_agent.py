import asyncio
import os
import sys
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
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


# Create one AutoGen assistant agent.
def create_agent(model_client) -> AssistantAgent:
    return AssistantAgent(
        name="basic_autogen_agent",
        model_client=model_client,
        system_message="You are a concise beginner-friendly assistant.",
    )


# Run a single AutoGen assistant response.
async def main() -> None:
    model_client = create_model_client()
    agent = create_agent(model_client)
    question = input("Ask a question: ").strip() or "Explain AutoGen in one paragraph."
    try:
        result = await agent.run(task=question)
        print("\nAgent:", result.messages[-1].content)
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
