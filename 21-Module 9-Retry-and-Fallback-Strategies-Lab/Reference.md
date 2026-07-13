# 21-Module 9-Retry-and-Fallback-Strategies-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Implement retry and fallback strategies using LangGraph.
This lab demonstrates how production AI workflows can recover from temporary dependency failures and switch to a fallback path when the primary service is unavailable.
Create a resilient AI workflow for incident summary generation.
The system should:

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `config/__init__.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Code:

```python


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import OpenAI`

Functions:

- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
EMBEDDING_MODEL = os.environ.get("Embedding_Model", "text-embedding-3-large")


def create_openai_client() -> OpenAI:
    # Creates an OpenAI-compatible client for Azure AI Foundry endpoint.
    return OpenAI(
        base_url=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
    )

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/resiliency_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.resiliency_models import ResiliencyState`
- `from nodes.resiliency_nodes import fallback_node, final_node, primary_node, route_after_primary`

Functions:

- `build_resiliency_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.resiliency_models import ResiliencyState
from nodes.resiliency_nodes import fallback_node, final_node, primary_node, route_after_primary


def build_resiliency_graph():
    # Builds a LangGraph workflow with conditional retry and fallback routing.
    graph = StateGraph(ResiliencyState)
    graph.add_node("primary", primary_node)
    graph.add_node("fallback", fallback_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("primary")
    graph.add_conditional_edges(
        "primary",
        route_after_primary,
        {
            "retry": "primary",
            "fallback": "fallback",
            "final": "final",
        },
    )
    graph.add_edge("fallback", "final")
    graph.add_edge("final", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from graphs.resiliency_graph import build_resiliency_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from graphs.resiliency_graph import build_resiliency_graph


DEFAULT_TASK = (
    "Generate an executive incident summary for a payment API outage. "
    "Include customer impact, immediate mitigation, owner, and next review time."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the retry and fallback lab.
    print("Lab 21: Retry And Fallback Strategies\n")
    print("Tip: include 'force fallback' in the task to test the fallback path.\n")
    task = input(f"Enter production task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    app = build_resiliency_graph()
    result = app.invoke(
        {
            "task": task,
            "attempt": 0,
            "max_attempts": 2,
            "primary_result": "",
            "fallback_result": "",
            "final_answer": "",
            "error_log": [],
            "status": "not_started",
        }
    )

    print("\n--- Final Status ---\n", result["status"])
    print("\n--- Error Log ---")
    for error in result["error_log"]:
        print("-", error)
    print("\n--- Primary Result ---\n", result["primary_result"])
    print("\n--- Fallback Result ---\n", result["fallback_result"])
    print("\n--- Final Resiliency Report ---\n", result["final_answer"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/resiliency_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `ResiliencyState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class ResiliencyState(TypedDict):
    # Shared state for retry, fallback, and final response nodes.
    task: str
    attempt: int
    max_attempts: int
    primary_result: str
    fallback_result: str
    final_answer: str
    error_log: list[str]
    status: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/resiliency_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.resiliency_models import ResiliencyState`
- `from services.dependency_service import call_primary_dependency`
- `from services.llm_service import ask_model`

Functions:

- `primary_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `route_after_primary()`: Chooses the next workflow branch or target agent based on the current state/input.
- `fallback_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.resiliency_models import ResiliencyState
from services.dependency_service import call_primary_dependency
from services.llm_service import ask_model


def primary_node(state: ResiliencyState) -> ResiliencyState:
    # Calls the primary dependency and records whether retry or fallback is required.
    state["attempt"] += 1

    try:
        dependency_result = call_primary_dependency(state["task"], state["attempt"])
        state["primary_result"] = ask_model(
            "You are a production AI assistant.",
            (
                "Create a clear response using this successful dependency result.\n\n"
                f"Dependency result: {dependency_result}"
            ),
        )
        state["status"] = "primary_success"
    except Exception as exc:
        state["error_log"].append(f"Attempt {state['attempt']} failed: {exc}")
        if state["attempt"] < state["max_attempts"]:
            state["status"] = "retry_needed"
        else:
            state["status"] = "fallback_needed"

    return state


def route_after_primary(state: ResiliencyState) -> str:
    # Chooses the next LangGraph edge based on retry/fallback status.
    if state["status"] == "retry_needed":
        return "retry"
    if state["status"] == "fallback_needed":
        return "fallback"
    return "final"


def fallback_node(state: ResiliencyState) -> ResiliencyState:
    # Uses a fallback response path when the primary dependency is unavailable.
    state["fallback_result"] = ask_model(
        "You are a fallback AI assistant for a degraded production workflow.",
        (
            "The primary dependency failed. Create a safe fallback response. "
            "Mention that the workflow should continue in degraded mode, capture the task, "
            "notify operations, and retry later.\n\n"
            f"Task: {state['task']}\n"
            f"Errors: {state['error_log']}"
        ),
    )
    state["status"] = "fallback_success"
    return state


def final_node(state: ResiliencyState) -> ResiliencyState:
    # Creates the final resiliency report for the lab participant.
    state["final_answer"] = ask_model(
        "You are a reliability engineering trainer.",
        (
            "Explain the retry and fallback workflow used here. Include attempts, status, "
            "error log, final result, and production reliability lessons.\n\n"
            f"Task: {state['task']}\n"
            f"Status: {state['status']}\n"
            f"Primary result: {state['primary_result']}\n"
            f"Fallback result: {state['fallback_result']}\n"
            f"Error log: {state['error_log']}"
        ),
    )
    return state

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/dependency_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `call_primary_dependency()`: Encapsulates reusable logic used by this lab.

Code:

```python
def call_primary_dependency(task: str, attempt: int) -> str:
    # Simulates an unstable primary AI dependency.
    # The first attempt fails to demonstrate retry behavior.
    # If the task contains "force fallback", every primary attempt fails.
    if "force fallback" in task.lower():
        raise RuntimeError("Primary dependency is unavailable. Circuit breaker is open.")

    if attempt == 1:
        raise RuntimeError("Temporary timeout from primary dependency.")

    return f"Primary dependency completed the task after attempt {attempt}: {task}"

```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import AZURE_OPENAI_DEPLOYMENT, create_openai_client`

Functions:

- `ask_model()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import AZURE_OPENAI_DEPLOYMENT, create_openai_client


client = create_openai_client()


def ask_model(system_message: str, user_message: str) -> str:
    # Sends one simple chat completion request to the configured Foundry model.
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

```


