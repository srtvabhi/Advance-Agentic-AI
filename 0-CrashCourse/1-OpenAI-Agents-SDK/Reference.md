# OpenAI Agents SDK Reference

This folder uses:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
```

## Local Environment

Each Python file in this folder loads configuration from this folder's own `.env` file:

```python
load_dotenv(Path(__file__).with_name(".env"), override=True)
```

This means the examples do not depend on the parent/global `.env` file. A virtual environment only provides installed packages; it does not provide Azure OpenAI settings.

## 1. Configure The SDK

Syntax:

```python
from openai import AsyncOpenAI
from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled

client = AsyncOpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
```

Example:

```python
def configure_agents_sdk() -> None:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    client = AsyncOpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)
```

## 2. Create A Single Agent

Syntax:

```python
from agents import Agent

agent = Agent(
    name="Agent Name",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="Agent instructions here.",
)
```

Example:

```python
agent = Agent(
    name="Basic Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="You are a helpful assistant. Keep answers short.",
)
```

## 3. Run An Agent

Syntax:

```python
from agents import Runner

result = await Runner.run(agent, user_question)
print(result.final_output)
```

Example:

```python
question = "Explain agentic AI in one paragraph."
result = await Runner.run(agent, question)
print(result.final_output)
```

## 4. Create A Tool

Syntax:

```python
from agents import function_tool

@function_tool
def tool_name(input_value: str) -> str:
    """Tool description."""
    return "tool result"
```

Example:

```python
@function_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression using numbers and + - * / ( )."""
    return calculate_expression(expression)
```

## 5. Attach Tools To An Agent

Syntax:

```python
agent = Agent(
    name="Tool Agent",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="Use tools when needed.",
    tools=[tool_one, tool_two],
)
```

Example:

```python
agent = Agent(
    name="Tool Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="Use calculator and weather tools when needed.",
    tools=[calculator, get_weather],
)
```

Note: In this crash-course folder, the tool functions are called manually before the final agent response for reliable Azure Foundry execution with `gpt-oss-120b`.

## 6. Multi-Agent Orchestration

Syntax:

```python
plan = await Runner.run(planner_agent, task)
execution = await Runner.run(executor_agent, plan.final_output)
review = await Runner.run(reviewer_agent, execution.final_output)
```

Example:

```python
plan = await Runner.run(create_planner(), task)
execution = await Runner.run(create_executor(), plan.final_output)
review = await Runner.run(create_reviewer(), execution.final_output)
```
