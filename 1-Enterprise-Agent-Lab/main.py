import asyncio

from agent.enterprise_agent import create_enterprise_agent
from config.settings import configure_openai_client
from agents import Runner


# Enterprise Agent Lab
# This is the application entry point.
# It loads settings, creates the agent, and starts a simple chat loop.


async def main() -> None:
    configure_openai_client()
    agent = create_enterprise_agent()

    print("Enterprise Agent Lab is ready.")
    print("Ask about time, math, weather, or web search.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        result = await Runner.run(agent, question)
        print("\nAgent:", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(main())

