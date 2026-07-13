# 10-AutoGen-Collaborative-Workflow-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build an AutoGen collaborative multi-agent workflow.
Design a collaborative AutoGen solution for enterprise loan application processing.
User Task
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

### `agents/team_agents.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from autogen_agentchat.agents import AssistantAgent`

Functions:

- `create_business_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_architect_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_security_agent()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_coordinator_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from autogen_agentchat.agents import AssistantAgent


def create_business_agent(model_client):
    return AssistantAgent(
        name="business_analyst",
        model_client=model_client,
        system_message=(
            "You are a business analyst. Explain business goals, users, value, "
            "success metrics, and adoption risks. Keep your answer under 8 short bullets."
        ),
    )


def create_architect_agent(model_client):
    return AssistantAgent(
        name="solution_architect",
        model_client=model_client,
        system_message=(
            "You are a solution architect. Explain systems, APIs, data flow, "
            "agent responsibilities, and integration points. Keep your answer under 8 short bullets."
        ),
    )


def create_security_agent(model_client):
    return AssistantAgent(
        name="security_reviewer",
        model_client=model_client,
        system_message=(
            "You are a security reviewer. Explain privacy, compliance, access control, "
            "audit logging, and governance risks. Keep your answer under 8 short bullets."
        ),
    )


def create_coordinator_agent(model_client):
    return AssistantAgent(
        name="coordinator",
        model_client=model_client,
        system_message=(
            "You are the coordinator. Combine the other agents' ideas into one final "
            "enterprise recommendation with clear next steps. Keep your answer under 10 short bullets."
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
- `from orchestration.group_chat import create_group_chat`
- `from services.output_service import format_team_messages`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from config.settings import create_model_client
from orchestration.group_chat import create_group_chat
from services.output_service import format_team_messages


DEFAULT_TASK = (
    "Design a collaborative AutoGen solution for enterprise loan application processing. "
    "Include business workflow, technical architecture, security controls, and final recommendation."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 10: AutoGen Collaborative Multi-Agent Workflow\n")
    task = input(f"Enter task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    team = create_group_chat(model_client)

    try:
        result = await team.run(task=task)
        print("\n--- AutoGen Group Conversation ---\n")
        print(format_team_messages(result.messages))
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

### `models/conversation_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `AgentMessage`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


@dataclass
class AgentMessage:
    source: str
    content: str

    def to_text(self) -> str:
        return f"\n--- {self.source} ---\n{self.content}"


```

### `orchestration/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `orchestration/group_chat.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from autogen_agentchat.conditions import MaxMessageTermination`
- `from autogen_agentchat.teams import RoundRobinGroupChat`
- `from agents.team_agents import (`

Functions:

- `create_group_chat()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from agents.team_agents import (
    create_architect_agent,
    create_business_agent,
    create_coordinator_agent,
    create_security_agent,
)


def create_group_chat(model_client):
    agents = [
        create_business_agent(model_client),
        create_architect_agent(model_client),
        create_security_agent(model_client),
        create_coordinator_agent(model_client),
    ]

    return RoundRobinGroupChat(
        participants=agents,
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

- `from models.conversation_models import AgentMessage`

Functions:

- `format_team_messages()`: Encapsulates reusable logic used by this lab.

Code:

```python
from models.conversation_models import AgentMessage


def format_team_messages(messages) -> str:
    formatted = []
    for message in messages:
        message_type = type(message).__name__
        if message_type == "ThoughtEvent":
            continue

        content = getattr(message, "content", "")
        source = getattr(message, "source", "unknown")
        if content:
            formatted.append(AgentMessage(source=source, content=str(content)).to_text())
    return "\n".join(formatted)

```


