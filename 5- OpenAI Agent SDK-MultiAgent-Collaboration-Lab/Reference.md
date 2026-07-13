# 5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Create a multi-agent collaboration pipeline using the OpenAI Agents SDK.
This lab demonstrates concurrent orchestration:
1. Business Agent analyzes business value.
2. Technical Agent analyzes architecture.

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
        name="Business Agent",
        model=get_model_name(),
        instructions=(
            "You are a business analyst agent. Identify business goals, users, "
            "success metrics, and adoption considerations. Keep it concise."
        ),
    )


```

### `agent/coordinator_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_coordinator_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


def create_coordinator_agent() -> Agent:
    return Agent(
        name="Coordinator Agent",
        model=get_model_name(),
        instructions=(
            "You are a coordinator agent. Combine outputs from business, technical, "
            "and risk agents into one clear final recommendation for enterprise leaders."
        ),
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
        name="Risk Agent",
        model=get_model_name(),
        instructions=(
            "You are a risk and governance agent. Identify security, privacy, "
            "compliance, operational, and quality risks. Keep it concise."
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
        name="Technical Agent",
        model=get_model_name(),
        instructions=(
            "You are a technical architecture agent. Identify systems, data, APIs, "
            "tools, orchestration approach, and integration points. Keep it concise."
        ),
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
- `from agent.coordinator_agent import create_coordinator_agent`
- `from agent.risk_agent import create_risk_agent`
- `from agent.technical_agent import create_technical_agent`
- `from config.settings import configure_openai_client`
- `from models.collaboration_models import CollaborationResult`
- `from agents import Runner`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from agent.business_agent import create_business_agent
from agent.coordinator_agent import create_coordinator_agent
from agent.risk_agent import create_risk_agent
from agent.technical_agent import create_technical_agent
from config.settings import configure_openai_client
from models.collaboration_models import CollaborationResult
from agents import Runner


# Lab 2: Multi-Agent Collaboration Pipeline
# Pattern: Concurrent orchestration + coordinator.


DEFAULT_SCENARIO = "Design an AI agent system for an enterprise HR helpdesk."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    configure_openai_client()

    business_agent = create_business_agent()
    technical_agent = create_technical_agent()
    risk_agent = create_risk_agent()
    coordinator_agent = create_coordinator_agent()

    print("Multi-Agent Collaboration Lab\n")
    scenario = input(f"Enter scenario, or press Enter for default:\n{DEFAULT_SCENARIO}\n\nScenario: ").strip()
    scenario = scenario or DEFAULT_SCENARIO

    # Run specialist agents at the same time.
    business_task = Runner.run(business_agent, scenario)
    technical_task = Runner.run(technical_agent, scenario)
    risk_task = Runner.run(risk_agent, scenario)

    business_result, technical_result, risk_result = await asyncio.gather(
        business_task,
        technical_task,
        risk_task,
    )

    print("\n--- Business Agent Output ---\n")
    print(business_result.final_output)
    print("\n--- Technical Agent Output ---\n")
    print(technical_result.final_output)
    print("\n--- Risk Agent Output ---\n")
    print(risk_result.final_output)

    coordinator_prompt = f"""
Scenario:
{scenario}

Business analysis:
{business_result.final_output}

Technical analysis:
{technical_result.final_output}

Risk analysis:
{risk_result.final_output}

Create one final recommendation.
"""

    final_result = await Runner.run(coordinator_agent, coordinator_prompt)
    print("\n--- Coordinator Final Output ---\n")
    print(final_result.final_output)

    collaboration = CollaborationResult(
        scenario=scenario,
        business_view=business_result.final_output,
        technical_view=technical_result.final_output,
        risk_view=risk_result.final_output,
        final_summary=final_result.final_output,
    )

    print("\n--- Final Collaboration Summary ---\n")
    print(collaboration.to_text())


if __name__ == "__main__":
    asyncio.run(main())

```

### `models/collaboration_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `CollaborationResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


@dataclass
class CollaborationResult:
    scenario: str
    business_view: str
    technical_view: str
    risk_view: str
    final_summary: str

    def to_text(self) -> str:
        return (
            f"Scenario:\n{self.scenario}\n\n"
            f"Business View:\n{self.business_view}\n\n"
            f"Technical View:\n{self.technical_view}\n\n"
            f"Risk View:\n{self.risk_view}\n\n"
            f"Final Summary:\n{self.final_summary}"
        )


```


