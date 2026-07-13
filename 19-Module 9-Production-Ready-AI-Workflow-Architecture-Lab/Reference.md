# 19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Design a production-ready AI workflow architecture using LangGraph.
Design an enterprise customer support AI assistant that handles high ticket volume, calls CRM tools, and needs production reliability.
Problem Statement
   |

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

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_embedding_model()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_embedding_model() -> str:
    load_environment()
    return os.environ.get("Embedding_Model") or os.environ.get("EMBEDDING_MODEL") or "text-embedding-3-large"

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/architecture_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.architecture_models import ArchitectureState`
- `from nodes.architecture_nodes import architecture_node, cost_latency_node, deployment_node, intake_node, reliability_node, summary_node`

Functions:

- `build_architecture_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.architecture_models import ArchitectureState
from nodes.architecture_nodes import architecture_node, cost_latency_node, deployment_node, intake_node, reliability_node, summary_node


def build_architecture_graph():
    graph = StateGraph(ArchitectureState)
    graph.add_node("intake", intake_node)
    graph.add_node("architecture", architecture_node)
    graph.add_node("deployment", deployment_node)
    graph.add_node("reliability", reliability_node)
    graph.add_node("cost_latency", cost_latency_node)
    graph.add_node("summary", summary_node)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "architecture")
    graph.add_edge("architecture", "deployment")
    graph.add_edge("deployment", "reliability")
    graph.add_edge("reliability", "cost_latency")
    graph.add_edge("cost_latency", "summary")
    graph.add_edge("summary", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from graphs.architecture_graph import build_architecture_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from graphs.architecture_graph import build_architecture_graph


DEFAULT_PROBLEM = (
    "Design a production-ready AI workflow for an enterprise customer support assistant "
    "that handles 50,000 tickets per day, calls CRM tools, and needs high reliability."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 19: Production-Ready AI Workflow Architecture\n")
    problem = input(f"Enter architecture problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_architecture_graph()
    result = app.invoke(
        {
            "problem": problem,
            "intake_summary": "",
            "architecture_design": "",
            "deployment_pattern": "",
            "reliability_plan": "",
            "cost_latency_plan": "",
            "final_summary": "",
        }
    )

    print("\n--- Intake Summary ---\n", result["intake_summary"])
    print("\n--- Architecture Design ---\n", result["architecture_design"])
    print("\n--- Deployment Pattern ---\n", result["deployment_pattern"])
    print("\n--- Reliability Plan ---\n", result["reliability_plan"])
    print("\n--- Cost And Latency Plan ---\n", result["cost_latency_plan"])
    print("\n--- Final Production Summary ---\n", result["final_summary"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/architecture_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `ArchitectureState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class ArchitectureState(TypedDict):
    problem: str
    intake_summary: str
    architecture_design: str
    deployment_pattern: str
    reliability_plan: str
    cost_latency_plan: str
    final_summary: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/architecture_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.architecture_models import ArchitectureState`
- `from services.llm_service import ask_model`

Functions:

- `intake_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `architecture_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `deployment_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `reliability_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `cost_latency_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `summary_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.architecture_models import ArchitectureState
from services.llm_service import ask_model


def intake_node(state: ArchitectureState) -> ArchitectureState:
    state["intake_summary"] = ask_model(
        "You are a production AI architect. Summarize the business goal, users, workload, and critical risks in 5 bullets.",
        state["problem"],
    )
    return state


def architecture_node(state: ArchitectureState) -> ArchitectureState:
    state["architecture_design"] = ask_model(
        "Design a production-grade AI workflow architecture. Include API layer, orchestration, model service, tools, data, observability, and security. Keep under 180 words.",
        state["intake_summary"],
    )
    return state


def deployment_node(state: ArchitectureState) -> ArchitectureState:
    state["deployment_pattern"] = ask_model(
        "Recommend stateless and stateful deployment patterns for this AI workflow. Mention containers, queues, state store, and scaling. Keep under 160 words.",
        state["architecture_design"],
    )
    return state


def reliability_node(state: ArchitectureState) -> ArchitectureState:
    state["reliability_plan"] = ask_model(
        "Create a reliability engineering plan. Include SLOs, dependency monitoring, retries, fallbacks, circuit breakers, and incident response. Keep under 160 words.",
        state["deployment_pattern"],
    )
    return state


def cost_latency_node(state: ArchitectureState) -> ArchitectureState:
    state["cost_latency_plan"] = ask_model(
        "Create cost and latency optimization guidance for the AI workflow. Include caching, batching, routing, token control, and async processing. Keep under 160 words.",
        state["reliability_plan"],
    )
    return state


def summary_node(state: ArchitectureState) -> ArchitectureState:
    state["final_summary"] = ask_model(
        "Combine the architecture, deployment, reliability, cost, and latency guidance into one concise production design summary.",
        (
            f"Architecture:\n{state['architecture_design']}\n\n"
            f"Deployment:\n{state['deployment_pattern']}\n\n"
            f"Reliability:\n{state['reliability_plan']}\n\n"
            f"Cost and latency:\n{state['cost_latency_plan']}"
        ),
    )
    return state

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_model()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import create_openai_client, get_model_name


def ask_model(system_prompt: str, user_prompt: str) -> str:
    client = create_openai_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""

```


