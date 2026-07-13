# 8-LangGraph-Conditional-Routing-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Create conditional agent routing flows using LangGraph.
User Question
   |
   v

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

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> AsyncOpenAI:
    load_environment()
    return AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


```

### `graph/routing_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, START, StateGraph`
- `from models.state_models import RoutingState`
- `from nodes.business_node import business_node`
- `from nodes.final_node import final_node`
- `from nodes.general_node import general_node`
- `from nodes.risk_node import risk_node`
- `from nodes.router_node import router_node`
- `from nodes.technical_node import technical_node`

Functions:

- `choose_route()`: Chooses the next workflow branch or target agent based on the current state/input.
- `build_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, START, StateGraph

from models.state_models import RoutingState
from nodes.business_node import business_node
from nodes.final_node import final_node
from nodes.general_node import general_node
from nodes.risk_node import risk_node
from nodes.router_node import router_node
from nodes.technical_node import technical_node


def choose_route(state: RoutingState) -> str:
    return state["route"]


def build_graph():
    graph = StateGraph(RoutingState)

    graph.add_node("router", router_node)
    graph.add_node("business", business_node)
    graph.add_node("technical", technical_node)
    graph.add_node("risk", risk_node)
    graph.add_node("general", general_node)
    graph.add_node("final", final_node)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        choose_route,
        {
            "business": "business",
            "technical": "technical",
            "risk": "risk",
            "general": "general",
        },
    )

    graph.add_edge("business", "final")
    graph.add_edge("technical", "final")
    graph.add_edge("risk", "final")
    graph.add_edge("general", "final")
    graph.add_edge("final", END)

    return graph.compile()


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from graph.routing_graph import build_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from graph.routing_graph import build_graph


DEFAULT_QUESTION = "What security controls are needed for a payroll automation agent?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 8: LangGraph Conditional Agent Routing\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    app = build_graph()
    result = await app.ainvoke({"question": question})

    print("\n--- Final Response ---\n")
    print(result["final_response"])


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/state_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import Literal, TypedDict`

Classes:

- `RoutingState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import Literal, TypedDict


RouteName = Literal["business", "technical", "risk", "general"]


class RoutingState(TypedDict, total=False):
    question: str
    route: RouteName
    answer: str
    final_response: str


```

### `nodes/business_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`
- `from services.llm_service import ask_llm`

Functions:

- `business_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState
from services.llm_service import ask_llm


async def business_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a business specialist. Focus on business goals, ROI, users, and adoption.",
        state["question"],
    )
    return {"answer": answer}


```

### `nodes/final_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`

Functions:

- `final_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState


async def final_node(state: RoutingState) -> RoutingState:
    return {
        "final_response": (
            f"Route selected: {state['route']}\n\n"
            f"Answer:\n{state['answer']}"
        )
    }


```

### `nodes/general_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`
- `from services.llm_service import ask_llm`

Functions:

- `general_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState
from services.llm_service import ask_llm


async def general_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a helpful general assistant. Answer simply and clearly.",
        state["question"],
    )
    return {"answer": answer}


```

### `nodes/risk_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`
- `from services.llm_service import ask_llm`

Functions:

- `risk_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState
from services.llm_service import ask_llm


async def risk_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a risk specialist. Focus on security, privacy, compliance, and governance.",
        state["question"],
    )
    return {"answer": answer}


```

### `nodes/router_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`
- `from services.llm_service import ask_llm`
- `from services.routing_service import normalize_route`

Functions:

- `router_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState
from services.llm_service import ask_llm
from services.routing_service import normalize_route


async def router_node(state: RoutingState) -> RoutingState:
    route_text = await ask_llm(
        "You are a router. Return only one word: business, technical, risk, or general.",
        state["question"],
    )
    return {"route": normalize_route(route_text)}


```

### `nodes/technical_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import RoutingState`
- `from services.llm_service import ask_llm`

Functions:

- `technical_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import RoutingState
from services.llm_service import ask_llm


async def technical_node(state: RoutingState) -> RoutingState:
    answer = await ask_llm(
        "You are a technical specialist. Focus on APIs, data, architecture, and implementation.",
        state["question"],
    )
    return {"answer": answer}


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_llm()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import create_openai_client, get_model_name


async def ask_llm(system_prompt: str, user_prompt: str) -> str:
    client = create_openai_client()
    response = await client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


```

### `services/routing_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `normalize_route()`: Encapsulates reusable logic used by this lab.

Code:

```python
def normalize_route(text: str) -> str:
    route = text.lower()
    if "technical" in route:
        return "technical"
    if "business" in route:
        return "business"
    if "risk" in route:
        return "risk"
    return "general"


```


