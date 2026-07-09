import asyncio

from agent.stateful_agent import create_stateful_agent
from config.settings import configure_openai_client
from Memory import ConversationMemory
from agents import Runner


# Stateful Agent Lab
# Objective: Build a stateful agent workflow design.
# This lab shows how to keep previous conversation messages in memory.


async def main() -> None:
    configure_openai_client()
    agent = create_stateful_agent()
    memory = ConversationMemory()

    print("Stateful Agent Lab is ready.")
    print("The agent remembers earlier messages in this session.")
    print("Type 'memory' to view stored conversation.")
    print("Type 'clear' to clear memory.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            break

        if user_message.lower() == "memory":
            print("\nStored Memory:\n")
            print(memory.show_memory())
            print()
            continue

        if user_message.lower() == "clear":
            memory.clear()
            print("\nMemory cleared.\n")
            continue

        if not user_message:
            continue

        # Step 1: Add the user message to memory.
        memory.add_user_message(user_message)

        # Step 2: Send full memory to the agent.
        result = await Runner.run(agent, memory.get_items())

        print("\nAgent:", result.final_output, "\n")

        # Step 3: Update memory with the complete conversation state.
        memory.update_from_result(result)


if __name__ == "__main__":
    asyncio.run(main())

