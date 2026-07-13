# 2- OpenAI Agent SDK-Stateful-Agent-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build a stateful agent workflow design using the OpenAI Agents SDK.
This lab demonstrates how an agent can remember previous conversation messages during the same running session.
This type of memory is called:
- Short-term memory

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

### `agent/stateful_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`

Functions:

- `create_stateful_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name


# This file defines the stateful workflow agent.
# The memory is handled in Memory.py and passed to this agent from main.py.


def create_stateful_agent() -> Agent:
    return Agent(
        name="Stateful Workflow Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful stateful workflow assistant. "
            "Use the previous conversation messages to answer follow-up questions. "
            "Explain stateful agent concepts in simple language for learners. "
            "When asked, identify what information you remember from the conversation."
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
- `from agents import (`

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

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


# This file keeps configuration in one place.
# This lab loads only its own .env file.


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
- `from agent.stateful_agent import create_stateful_agent`
- `from config.settings import configure_openai_client`
- `from Memory import ConversationMemory`
- `from agents import Runner`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio

from agent.stateful_agent import create_stateful_agent
from config.settings import configure_openai_client
from Memory import ConversationMemory
from agents import Runner


# Stateful Agent Lab
# Objective: Build a stateful agent workflow design.
# This lab shows how to keep previous conversation messages in memory.


async def main() -> None:
    configure_openai_client()
    agent = create_stateful_agent()
    memory = ConversationMemory()

    print("Stateful Agent Lab is ready.")
    print("The agent remembers earlier messages in this session.")
    print("Type 'memory' to view stored conversation.")
    print("Type 'clear' to clear memory.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            break

        if user_message.lower() == "memory":
            print("\nStored Memory:\n")
            print(memory.show_memory())
            print()
            continue

        if user_message.lower() == "clear":
            memory.clear()
            print("\nMemory cleared.\n")
            continue

        if not user_message:
            continue

        # Step 1: Add the user message to memory.
        memory.add_user_message(user_message)

        # Step 2: Send full memory to the agent.
        result = await Runner.run(agent, memory.get_items())

        print("\nAgent:", result.final_output, "\n")

        # Step 3: Update memory with the complete conversation state.
        memory.update_from_result(result)


if __name__ == "__main__":
    asyncio.run(main())


```

### `Memory.py`

Role: Memory layer. It stores or retrieves conversation/workflow state.

Key imports:

- `from models.conversation_models import MemoryItem`

Classes:

- `ConversationMemory`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from models.conversation_models import MemoryItem


# Memory.py
# This class stores previous conversation messages.
# It acts as short-term memory for the current terminal session.


class ConversationMemory:
    def __init__(self) -> None:
        self.input_items = []

    def add_user_message(self, message: str) -> None:
        """Save the latest user message."""
        self.input_items.append({"role": "user", "content": message})

    def get_items(self) -> list:
        """Return all messages stored in memory."""
        return self.input_items

    def update_from_result(self, result) -> None:
        """Store the updated conversation returned by the Agents SDK."""
        self.input_items = result.to_input_list()

    def clear(self) -> None:
        """Clear all stored conversation messages."""
        self.input_items = []

    def show_memory(self) -> str:
        """Show memory in a learner-friendly format."""
        if not self.input_items:
            return "No messages stored yet."

        readable_items = []
        for item in self.input_items:
            memory_item = MemoryItem.from_agent_item(item)
            readable_items.append(memory_item.to_text())

        return "\n".join(readable_items)


```

### `models/conversation_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `MemoryItem`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


# Models keep conversation memory data organized.
# This is intentionally simple for participants.


@dataclass
class MemoryItem:
    role: str
    content: str

    @classmethod
    def from_agent_item(cls, item: dict) -> "MemoryItem":
        role = item.get("role", item.get("type", "unknown"))
        content = item.get("content", "")

        if isinstance(content, list):
            content = " ".join(str(part) for part in content)

        return cls(role=role, content=str(content))

    def to_text(self) -> str:
        return f"{self.role}: {self.content}"


```


