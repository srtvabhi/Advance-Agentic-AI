import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from openai import OpenAI


class AgentState(TypedDict):
    question: str
    answer: str


# Load only this folder's .env file and create an OpenAI client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Node: call the model and save the answer into graph state.
def assistant_node(state: AgentState) -> AgentState:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are a concise beginner-friendly assistant."},
            {"role": "user", "content": state["question"]},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state


# Build a one-node LangGraph workflow.
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("assistant", assistant_node)
    graph.set_entry_point("assistant")
    graph.add_edge("assistant", END)
    return graph.compile()


# Run the graph with user input.
def main() -> None:
    question = input("Ask a question: ").strip() or "Explain LangGraph in one paragraph."
    result = build_graph().invoke({"question": question, "answer": ""})
    print("\nAgent:", result["answer"])


if __name__ == "__main__":
    main()

