# 20-Module 9-Scalable-AI-Orchestration-Pipeline-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build a scalable AI orchestration pipeline using LangGraph.
This lab demonstrates how production AI systems can process events from a queue, route work to the right worker pool, and apply scaling, latency, and cost controls.
Design a scalable AI pipeline for insurance claim intake.
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

### `graphs/pipeline_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.pipeline_models import PipelineState`
- `from nodes.pipeline_nodes import final_report_node, receive_events_node, routing_node, scaling_node, worker_pool_node`

Functions:

- `build_pipeline_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.pipeline_models import PipelineState
from nodes.pipeline_nodes import final_report_node, receive_events_node, routing_node, scaling_node, worker_pool_node


def build_pipeline_graph():
    # Builds a sequential LangGraph workflow for scalable queue-based orchestration.
    graph = StateGraph(PipelineState)
    graph.add_node("receive_events", receive_events_node)
    graph.add_node("routing", routing_node)
    graph.add_node("worker_pool", worker_pool_node)
    graph.add_node("scaling", scaling_node)
    graph.add_node("final_report", final_report_node)

    graph.set_entry_point("receive_events")
    graph.add_edge("receive_events", "routing")
    graph.add_edge("routing", "worker_pool")
    graph.add_edge("worker_pool", "scaling")
    graph.add_edge("scaling", "final_report")
    graph.add_edge("final_report", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from graphs.pipeline_graph import build_pipeline_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from graphs.pipeline_graph import build_pipeline_graph


DEFAULT_OBJECTIVE = (
    "Build a scalable AI orchestration pipeline for insurance claim intake. "
    "The system must process events from a queue, route high-risk claims, "
    "scale workers, and control latency and cost."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the scalable orchestration lab.
    print("Lab 20: Scalable AI Orchestration Pipeline\n")
    objective = input(f"Enter pipeline objective, or press Enter for default:\n{DEFAULT_OBJECTIVE}\n\nObjective: ").strip()
    objective = objective or DEFAULT_OBJECTIVE

    app = build_pipeline_graph()
    result = app.invoke(
        {
            "objective": objective,
            "events": [],
            "queue_summary": "",
            "routing_plan": "",
            "worker_pool_plan": "",
            "scaling_plan": "",
            "final_report": "",
        }
    )

    print("\n--- Queue Summary ---\n", result["queue_summary"])
    print("\n--- Routing Plan ---\n", result["routing_plan"])
    print("\n--- Worker Pool Plan ---\n", result["worker_pool_plan"])
    print("\n--- Scaling Plan ---\n", result["scaling_plan"])
    print("\n--- Final Pipeline Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/pipeline_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `PipelineState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class PipelineState(TypedDict):
    # Shared LangGraph state passed between all orchestration nodes.
    objective: str
    events: list[dict]
    queue_summary: str
    routing_plan: str
    worker_pool_plan: str
    scaling_plan: str
    final_report: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/pipeline_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.pipeline_models import PipelineState`
- `from services.llm_service import ask_model`
- `from services.queue_service import load_sample_events, summarize_events`

Functions:

- `receive_events_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `routing_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `worker_pool_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `scaling_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_report_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.pipeline_models import PipelineState
from services.llm_service import ask_model
from services.queue_service import load_sample_events, summarize_events


def receive_events_node(state: PipelineState) -> PipelineState:
    # Loads sample events to demonstrate queue-based orchestration.
    events = load_sample_events()
    state["events"] = events
    state["queue_summary"] = summarize_events(events)
    return state


def routing_node(state: PipelineState) -> PipelineState:
    # Designs routing rules for each event type and priority.
    state["routing_plan"] = ask_model(
        "You are an enterprise AI routing architect.",
        (
            "Create a routing plan for these queue events. Include priority handling, "
            "event categories, and which worker lane should process each event.\n\n"
            f"Objective: {state['objective']}\n"
            f"Queue summary: {state['queue_summary']}\n"
            f"Events: {state['events']}"
        ),
    )
    return state


def worker_pool_node(state: PipelineState) -> PipelineState:
    # Designs worker pools for distributed event processing.
    state["worker_pool_plan"] = ask_model(
        "You are a distributed systems engineer designing AI worker pools.",
        (
            "Convert the routing plan into worker pool design. Include stateless workers, "
            "stateful tracking, concurrency, and back-pressure handling.\n\n"
            f"Routing plan:\n{state['routing_plan']}"
        ),
    )
    return state


def scaling_node(state: PipelineState) -> PipelineState:
    # Adds production scalability, latency, and cost controls.
    state["scaling_plan"] = ask_model(
        "You are a production AI reliability engineer.",
        (
            "Create a scalability plan for this AI orchestration pipeline. Include autoscaling, "
            "queue depth metrics, cost optimization, latency optimization, and dependency limits.\n\n"
            f"Worker pool plan:\n{state['worker_pool_plan']}"
        ),
    )
    return state


def final_report_node(state: PipelineState) -> PipelineState:
    # Produces the final learner-friendly pipeline summary.
    state["final_report"] = ask_model(
        "You are a technical trainer explaining production AI orchestration.",
        (
            "Create a concise final report for participants. Explain the queue-based pipeline, "
            "routing, workers, scaling, and reliability considerations.\n\n"
            f"Objective: {state['objective']}\n"
            f"Queue summary: {state['queue_summary']}\n"
            f"Routing plan:\n{state['routing_plan']}\n"
            f"Worker pool plan:\n{state['worker_pool_plan']}\n"
            f"Scaling plan:\n{state['scaling_plan']}"
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

### `services/queue_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `load_sample_events()`: Encapsulates reusable logic used by this lab.
- `summarize_events()`: Encapsulates reusable logic used by this lab.

Code:

```python
def load_sample_events() -> list[dict]:
    # Simulates events that would normally come from Azure Service Bus, Kafka, or RabbitMQ.
    return [
        {"id": "CLM-1001", "type": "insurance_claim", "priority": "high", "region": "US", "amount": 25000},
        {"id": "CLM-1002", "type": "insurance_claim", "priority": "medium", "region": "EU", "amount": 8000},
        {"id": "CLM-1003", "type": "fraud_review", "priority": "critical", "region": "US", "amount": 75000},
        {"id": "CLM-1004", "type": "document_check", "priority": "low", "region": "APAC", "amount": 1200},
        {"id": "CLM-1005", "type": "insurance_claim", "priority": "high", "region": "EU", "amount": 18000},
    ]


def summarize_events(events: list[dict]) -> str:
    # Creates a small deterministic queue summary before the LLM planning steps.
    total = len(events)
    critical = sum(1 for event in events if event["priority"] == "critical")
    high = sum(1 for event in events if event["priority"] == "high")
    regions = sorted({event["region"] for event in events})
    return f"Loaded {total} events. Critical={critical}, High={high}, Regions={', '.join(regions)}."

```


