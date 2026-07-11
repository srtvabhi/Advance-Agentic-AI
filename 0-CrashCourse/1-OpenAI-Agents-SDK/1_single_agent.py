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


# Create one basic assistant agent.
def create_agent() -> Agent:
    return Agent(
        name="Basic Assistant",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="You are a helpful assistant. Keep answers short and beginner friendly.",
    )


# Run the agent with a simple user question.
async def main() -> None:
    configure_agents_sdk()
    agent = create_agent()
    question = input("Ask a question: ").strip() or "Explain agentic AI in one paragraph."
    result = await Runner.run(agent, question)
    print("\nAgent:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

