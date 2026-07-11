import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"

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


# Tool: calculate simple arithmetic expressions safely.
def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


# Tool: call OpenWeatherMap and return current weather for a city.
def get_weather(city: str) -> str:
    params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return f"{data['name']}: {data['weather'][0]['description']}, {data['main']['temp']} C."
    except Exception as exc:
        return f"Weather API error: {exc}"


# Create one AutoGen assistant and attach tools.
def create_agent(model_client) -> AssistantAgent:
    return AssistantAgent(
        name="tool_autogen_agent",
        model_client=model_client,
        tools=[calculator, get_weather],
        max_tool_iterations=3,
        system_message="Use tools for math and weather questions. Keep answers short.",
    )


# Run a tool-enabled AutoGen assistant.
async def main() -> None:
    model_client = create_model_client()
    agent = create_agent(model_client)
    question = input("Ask math or weather question: ").strip() or "Calculate 12 * 9 and get weather in Mumbai."
    try:
        result = await agent.run(task=question)
        print("\nAgent:", result.messages[-1].content)
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
