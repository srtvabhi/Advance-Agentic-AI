# 12-AutoGen-Autonomous-Ecosystem-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Create an autonomous task-solving agent ecosystem using AutoGen.
Investigate a payment API slowdown, open an incident, notify the team, analyze likely root cause, and prepare an update.
Incident Task
   |

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
autogen-agentchat==0.7.5
autogen-ext==0.7.5

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `agents/__init__.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Code:

```python


```

### `agents/ecosystem_agents.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from autogen_agentchat.agents import AssistantAgent`
- `from tools.incident_tools import (`

Functions:

- `create_operations_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_root_cause_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_comms_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_manager_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from autogen_agentchat.agents import AssistantAgent

from tools.incident_tools import (
    check_service_health,
    create_incident_ticket,
    notify_response_team,
)


def create_operations_agent(model_client):
    return AssistantAgent(
        name="operations_agent",
        model_client=model_client,
        tools=[check_service_health, create_incident_ticket, notify_response_team],
        max_tool_iterations=3,
        system_message=(
            "You are an autonomous operations agent. Use your tools to check health, "
            "create an incident ticket, and notify the response team when the task describes an outage. "
            "Keep your final message under 8 short bullets."
        ),
    )


def create_root_cause_agent(model_client):
    return AssistantAgent(
        name="root_cause_agent",
        model_client=model_client,
        system_message=(
            "You are a root cause analyst. Review the operations findings and propose likely causes, "
            "mitigation steps, and validation checks. Keep your answer under 8 short bullets."
        ),
    )


def create_comms_agent(model_client):
    return AssistantAgent(
        name="communications_agent",
        model_client=model_client,
        system_message=(
            "You are a communications agent. Draft a short internal stakeholder update with status, "
            "impact, action owner, and next update time. Keep your answer under 8 short bullets."
        ),
    )


def create_manager_agent(model_client):
    return AssistantAgent(
        name="incident_manager",
        model_client=model_client,
        system_message=(
            "You are the incident manager. Summarize the autonomous ecosystem's final action plan. "
            "Include ticket, diagnosis, mitigation, communication, and next steps. Keep your answer under 10 short bullets."
        ),
    )

```

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
- `from autogen_ext.models.openai import OpenAIChatCompletionClient`
- `from dotenv import load_dotenv`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_model_client()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
import os
from pathlib import Path

from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_model_client() -> OpenAIChatCompletionClient:
    load_environment()
    return OpenAIChatCompletionClient(
        model=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from config.settings import create_model_client`
- `from orchestration.ecosystem_chat import create_incident_ecosystem`
- `from services.output_service import format_transcript`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from config.settings import create_model_client
from orchestration.ecosystem_chat import create_incident_ecosystem
from services.output_service import format_transcript


DEFAULT_TASK = (
    "The payment API is slow and customers are reporting checkout failures. "
    "Autonomously investigate, open an incident, notify the team, analyze cause, and prepare an update."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 12: AutoGen Autonomous Task-Solving Ecosystem\n")
    task = input(f"Enter incident task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    team = create_incident_ecosystem(model_client)

    try:
        result = await team.run(task=task)
        print("\n--- Autonomous Ecosystem Transcript ---\n")
        print(format_transcript(result.messages).to_text())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/incident_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `IncidentRunResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


@dataclass
class IncidentRunResult:
    transcript: str

    def to_text(self) -> str:
        return self.transcript


```

### `orchestration/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `orchestration/ecosystem_chat.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from autogen_agentchat.conditions import MaxMessageTermination`
- `from autogen_agentchat.teams import RoundRobinGroupChat`
- `from agents.ecosystem_agents import (`

Functions:

- `create_incident_ecosystem()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from agents.ecosystem_agents import (
    create_comms_agent,
    create_manager_agent,
    create_operations_agent,
    create_root_cause_agent,
)


def create_incident_ecosystem(model_client):
    return RoundRobinGroupChat(
        participants=[
            create_operations_agent(model_client),
            create_root_cause_agent(model_client),
            create_comms_agent(model_client),
            create_manager_agent(model_client),
        ],
        termination_condition=MaxMessageTermination(5),
    )


```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/output_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from models.incident_models import IncidentRunResult`

Functions:

- `format_transcript()`: Encapsulates reusable logic used by this lab.

Code:

```python
from models.incident_models import IncidentRunResult


def format_transcript(messages) -> IncidentRunResult:
    lines = []
    for message in messages:
        message_type = type(message).__name__
        if message_type == "ThoughtEvent":
            continue

        source = getattr(message, "source", "unknown")
        content = getattr(message, "content", "")
        if content:
            lines.append(f"\n--- {source} ---\n{content}")
    return IncidentRunResult(transcript="\n".join(lines))

```

### `tools/__init__.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Code:

```python


```

### `tools/incident_tools.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Functions:

- `check_service_health()`: Runs service-level logic, often wrapping an external API or business rule.
- `create_incident_ticket()`: Factory/helper function that creates and returns a configured object used by the lab.
- `notify_response_team()`: Encapsulates reusable logic used by this lab.

Code:

```python
def check_service_health(service_name: str) -> str:
    """Check simulated service health."""
    return f"{service_name}: elevated latency detected, error rate 8%, database pool near capacity."


def create_incident_ticket(title: str, severity: str) -> str:
    """Create a simulated incident ticket."""
    return f"Created incident ticket INC-1042 with title '{title}' and severity '{severity}'."


def notify_response_team(message: str) -> str:
    """Notify a simulated response team."""
    return f"Notification sent to response team: {message}"


```


