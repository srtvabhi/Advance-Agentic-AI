import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Agent, Runner, function_tool, set_default_openai_api, set_default_openai_client, set_tracing_disabled


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"


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


# Helper: calculate simple arithmetic expressions safely.
def calculate_expression(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression. Use only numbers and + - * / ( )."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


# Helper: call OpenWeatherMap and return current weather for a city.
def fetch_weather(city: str) -> str:
    params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return (
            f"Weather in {data['name']}: {data['weather'][0]['description']}, "
            f"{data['main']['temp']} C, humidity {data['main']['humidity']}%."
        )
    except Exception as exc:
        return f"Weather API error: {exc}"


# Tool: expose calculator to the OpenAI Agents SDK.
@function_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression using numbers and + - * / ( )."""
    return calculate_expression(expression)


# Tool: expose weather lookup to the OpenAI Agents SDK.
@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city from OpenWeatherMap."""
    return fetch_weather(city)


# Helper: choose and run a tool before sending context to the agent.
def run_tool_for_question(question: str) -> str:
    lowered = question.lower()
    if "weather" in lowered:
        city = question.split(" in ")[-1].strip(" ?.") if " in " in lowered else "Delhi"
        return fetch_weather(city)
    if "calculate" in lowered:
        expression = lowered.replace("calculate", "").strip()
        return calculate_expression(expression)
    return "No tool was needed."


# Create one agent. The tool functions above are called manually for reliable Azure Foundry execution.
def create_agent() -> Agent:
    return Agent(
        name="Tool Assistant",
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions=(
            "You are a tool assistant. Explain the provided tool result clearly. "
            "The calculator and weather tools are used before you answer."
        ),
    )


# Run the tool-enabled agent.
async def main() -> None:
    configure_agents_sdk()
    agent = create_agent()
    question = input("Ask math or weather question: ").strip() or "Calculate 25 * 8 and get weather in Delhi."
    tool_result = run_tool_for_question(question)
    prompt = f"User question: {question}\nTool result: {tool_result}\nExplain the result."
    result = await Runner.run(agent, prompt)
    print("\nTool:", tool_result)
    print("\nAgent:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

