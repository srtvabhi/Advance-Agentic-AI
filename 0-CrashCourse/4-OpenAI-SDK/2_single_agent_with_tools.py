import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from openai import OpenAI


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"


# Load only this folder's .env file and create an OpenAI SDK client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


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


# Function: manually route to tools, then ask the model to summarize.
def ask_agent_with_tools(client: OpenAI, question: str) -> str:
    lowered = question.lower()
    if "weather" in lowered:
        city = question.split(" in ")[-1].strip(" ?.") if " in " in lowered else "Delhi"
        tool_result = get_weather(city)
    elif "calculate" in lowered:
        tool_result = calculator(lowered.replace("calculate", "").strip())
    else:
        tool_result = "No tool was needed."

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer using the provided tool result."},
            {"role": "user", "content": f"Question: {question}\nTool result: {tool_result}"},
        ],
    )
    return response.choices[0].message.content or ""


# Run the direct OpenAI SDK tool example.
def main() -> None:
    client = create_client()
    question = input("Ask math or weather question: ").strip() or "Calculate 99 / 3"
    print("\nAgent:", ask_agent_with_tools(client, question))


if __name__ == "__main__":
    main()

