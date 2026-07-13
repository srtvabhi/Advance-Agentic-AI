import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from agents import Agent, Runner, function_tool, set_default_openai_api, set_default_openai_client, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"

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

# 3. Create tools that the agent can use.
@function_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Invalid math expression."


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    query = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{query}", timeout=10) as response:
            data = json.load(response)
        return f"{data['name']}: {data['main']['temp']} C, {data['weather'][0]['description']}"
    except Exception:
        return "I could not get the weather for that city."


# 4. Give the tools to one agent and ask a question.
agent = Agent(
    name="Tool Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="Use the calculator or weather tool when needed. Keep answers simple.",
    tools=[calculator, get_weather],
)

question = input("Ask a math or weather question: ")
result = Runner.run_sync(agent, question)
print("Agent:", result.final_output)
