import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from openai import OpenAI


class MultiAgentState(TypedDict):
    task: str
    plan: str
    execution: str
    review: str


# Load only this folder's .env file and create an OpenAI client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Helper: call the model with a role-specific instruction.
def ask_model(system_prompt: str, user_prompt: str) -> str:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    )
    return response.choices[0].message.content or ""


# Node: planner agent creates the plan.
def planner_node(state: MultiAgentState) -> MultiAgentState:
    state["plan"] = ask_model("You are a planner. Create 5 short steps.", state["task"])
    return state


# Node: executor agent converts the plan into actions.
def executor_node(state: MultiAgentState) -> MultiAgentState:
    state["execution"] = ask_model("You are an executor. Add owners and actions.", state["plan"])
    return state


# Node: reviewer agent checks the workflow.
def reviewer_node(state: MultiAgentState) -> MultiAgentState:
    state["review"] = ask_model("You are a reviewer. Find risks and missing approvals.", state["execution"])
    return state


# Build a coordinated multi-agent graph.
def build_graph():
    graph = StateGraph(MultiAgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "reviewer")
    graph.add_edge("reviewer", END)
    return graph.compile()


# Run the multi-agent graph.
def main() -> None:
    task = input("Enter enterprise task: ").strip() or "Design an IT incident response workflow."
    result = build_graph().invoke({"task": task, "plan": "", "execution": "", "review": ""})
    print("\n--- Planner ---\n", result["plan"])
    print("\n--- Executor ---\n", result["execution"])
    print("\n--- Reviewer ---\n", result["review"])


if __name__ == "__main__":
    main()

