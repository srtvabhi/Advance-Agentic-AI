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
    route: str
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


# Node: decide which branch the graph should follow.
def router_node(state: ToolState) -> ToolState:
    question = state["question"].lower()
    if "weather" in question:
        state["route"] = "weather"
    elif "calculate" in question:
        state["route"] = "calculator"
    else:
        state["route"] = "no_tool"
    return state


# Conditional edge function: return the branch name selected by router_node.
def choose_tool_branch(state: ToolState) -> str:
    return state["route"]


# Branch node: call the calculator tool.
def calculator_node(state: ToolState) -> ToolState:
    expression = state["question"].lower().replace("calculate", "").strip()
    state["tool_result"] = calculator(expression)
    return state


# Branch node: call the weather tool.
def weather_node(state: ToolState) -> ToolState:
    question = state["question"].lower()
    city = state["question"].split(" in ")[-1].strip(" ?.") if " in " in question else "Delhi"
    state["tool_result"] = get_weather(city)
    return state


# Branch node: handle questions that do not need a tool.
def no_tool_node(state: ToolState) -> ToolState:
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


# Build a graph with conditional branches for calculator and weather tools.
def build_graph():
    graph = StateGraph(ToolState)
    graph.add_node("router", router_node)
    graph.add_node("calculator", calculator_node)
    graph.add_node("weather", weather_node)
    graph.add_node("no_tool", no_tool_node)
    graph.add_node("answer", answer_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        choose_tool_branch,
        {
            "calculator": "calculator",
            "weather": "weather",
            "no_tool": "no_tool",
        },
    )
    graph.add_edge("calculator", "answer")
    graph.add_edge("weather", "answer")
    graph.add_edge("no_tool", "answer")
    graph.add_edge("answer", END)
    return graph.compile()


# Print the LangGraph structure as Mermaid text.
# You can paste this Mermaid code into https://mermaid.live to see a visual diagram.
def show_graph(workflow) -> None:
    print("\nLangGraph structure:")
    print(workflow.get_graph().draw_mermaid())


# Run the graph with user input.
def main() -> None:
    workflow = build_graph()
    show_graph(workflow)

    question = input("Ask math or weather question: ").strip() or "Calculate 40 * 5"
    result = workflow.invoke({"question": question, "route": "", "tool_result": "", "answer": ""})
    print("\nTool name:", result["route"])
    print("Tool result:", result["tool_result"])
    print("Agent:", result["answer"])


if __name__ == "__main__":
    main()


# Sample prompts for testing calculator branch:
# 1. Calculate 40 * 5
# 2. Calculate 150 / 3 + 20
# 3. Calculate (25 + 15) * 2
#
# Sample prompts for testing weather branch:
# 1. What is the weather in Delhi?
# 2. Show me the weather in Mumbai
# 3. Get weather in London

