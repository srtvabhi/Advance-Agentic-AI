import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import json
import os
from pathlib import Path
from typing import TypedDict
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from openai import OpenAI


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"


class ToolState(TypedDict):
    question: str
    tool_result: str
    answer: str


# Load only this folder's .env file and create an OpenAI client.
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


# Node: choose a simple tool path based on the question text.
def tool_node(state: ToolState) -> ToolState:
    question = state["question"].lower()
    if "weather" in question:
        city = state["question"].split(" in ")[-1].strip(" ?.") if " in " in question else "Delhi"
        state["tool_result"] = get_weather(city)
    elif "calculate" in question:
        expression = state["question"].lower().replace("calculate", "").strip()
        state["tool_result"] = calculator(expression)
    else:
        state["tool_result"] = "No tool needed."
    return state


# Node: ask the model to explain the tool result.
def answer_node(state: ToolState) -> ToolState:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Explain the tool result in one short answer."},
            {"role": "user", "content": f"Question: {state['question']}\nTool result: {state['tool_result']}"},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state


# Build a graph with a tool node followed by an answer node.
def build_graph():
    graph = StateGraph(ToolState)
    graph.add_node("tool", tool_node)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("tool")
    graph.add_edge("tool", "answer")
    graph.add_edge("answer", END)
    return graph.compile()


# Run the graph with user input.
def main() -> None:
    question = input("Ask math or weather question: ").strip() or "Calculate 40 * 5"
    result = build_graph().invoke({"question": question, "tool_result": "", "answer": ""})
    print("\nTool:", result["tool_result"])
    print("Agent:", result["answer"])


if __name__ == "__main__":
    main()

