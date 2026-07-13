# 6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Implement dynamic routing between multiple agents using the OpenAI Agents SDK.
This lab demonstrates supervisor agent architecture:
1. Router Agent reads the user question.
2. Router Agent chooses the best specialist.

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `agent/business_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_business_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_business_agent() -> Agent:
    return Agent(
        name="Business Specialist",
        model=get_model_name(),
        instructions="You answer business process, ROI, adoption, and stakeholder questions.",
    )


```

### `agent/general_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_general_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_general_agent() -> Agent:
    return Agent(
        name="General Specialist",
        model=get_model_name(),
        instructions="You answer general questions clearly and simply.",
    )


```

### `agent/risk_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_risk_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_risk_agent() -> Agent:
    return Agent(
        name="Risk Specialist",
        model=get_model_name(),
        instructions="You answer security, compliance, privacy, safety, and governance questions.",
    )


```

### `agent/router_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_router_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_router_agent() -> Agent:
    return Agent(
        name="Supervisor Router Agent",
        model=get_model_name(),
        instructions=(
            "You are a supervisor router agent. Route the user question to the best specialist. "
            "Reply with only one route word: business, technical, risk, or general."
        ),
    )


```

### `agent/technical_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_technical_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_technical_agent() -> Agent:
    return Agent(
        name="Technical Specialist",
        model=get_model_name(),
        instructions="You answer architecture, integration, API, data, and implementation questions.",
    )


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Encapsulates reusable logic used by this lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def configure_openai_client() -> None:
    load_environment()
    client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from agent.business_agent import create_business_agent`
- `from agent.general_agent import create_general_agent`
- `from agent.risk_agent import create_risk_agent`
- `from agent.router_agent import create_router_agent`
- `from agent.technical_agent import create_technical_agent`
- `from config.settings import configure_openai_client`
- `from models.routing_models import RoutingDecision`
- `from services.routing_service import normalize_route`
- `from agents import Agent, Runner`

Functions:

- `select_agent()`: Encapsulates reusable logic used by this lab.
- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from agent.business_agent import create_business_agent
from agent.general_agent import create_general_agent
from agent.risk_agent import create_risk_agent
from agent.router_agent import create_router_agent
from agent.technical_agent import create_technical_agent
from config.settings import configure_openai_client
from models.routing_models import RoutingDecision
from services.routing_service import normalize_route
from agents import Agent, Runner


# Lab 3: Dynamic Routing Between Multiple Agents
# Pattern: Supervisor/router orchestration.


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def select_agent(route: str, agents_by_route: dict[str, Agent]) -> Agent:
    return agents_by_route.get(route, agents_by_route["general"])


async def main() -> None:
    configure_openai_client()

    router_agent = create_router_agent()
    agents_by_route = {
        "business": create_business_agent(),
        "technical": create_technical_agent(),
        "risk": create_risk_agent(),
        "general": create_general_agent(),
    }

    print("Dynamic Agent Routing Lab")
    print("Ask a business, technical, risk, or general question.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        route_result = await Runner.run(router_agent, question)
        route = normalize_route(route_result.final_output)
        selected_agent = select_agent(route, agents_by_route)

        print(f"[Router selected: {route} -> {selected_agent.name}]")

        answer_result = await Runner.run(selected_agent, question)

        decision = RoutingDecision(
            question=question,
            route=route,
            selected_agent=selected_agent.name,
            answer=answer_result.final_output,
        )

        print("\n" + decision.to_text() + "\n")


if __name__ == "__main__":
    asyncio.run(main())

```

### `models/routing_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `RoutingDecision`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


@dataclass
class RoutingDecision:
    question: str
    route: str
    selected_agent: str
    answer: str

    def to_text(self) -> str:
        return (
            f"Question: {self.question}\n"
            f"Route: {self.route}\n"
            f"Selected Agent: {self.selected_agent}\n\n"
            f"Answer:\n{self.answer}"
        )


```

### `services/routing_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `normalize_route()`: Encapsulates reusable logic used by this lab.

Code:

```python
# Converts router text into a stable route.
# This protects the app if the router adds extra words.


def normalize_route(route_text: str) -> str:
    route = route_text.lower().strip()

    if "technical" in route:
        return "technical"
    if "business" in route:
        return "business"
    if "risk" in route:
        return "risk"
    return "general"


```


