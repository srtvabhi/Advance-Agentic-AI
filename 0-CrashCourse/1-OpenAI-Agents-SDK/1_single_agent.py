import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled

# 1. Load settings from the .env file in this folder.
load_dotenv(Path(__file__).parent / ".env")

# 2. Connect the Agents SDK to Azure OpenAI.
client = AsyncOpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

# 3. Create one agent.
agent = Agent(
    name="Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="You are a helpful assistant. Give short and simple answers.",
)

# 4. Ask the agent a question and print its answer.
question = input("Ask a question: ")
result = Runner.run_sync(agent, question)
print("Agent:", result.final_output)

