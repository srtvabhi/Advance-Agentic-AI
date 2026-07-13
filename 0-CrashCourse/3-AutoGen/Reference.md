# AutoGen Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
autogen-agentchat==0.7.5
autogen-ext==0.7.5
```

## Local Environment

Each Python file in this folder loads configuration from this folder's own `.env` file:

```python
load_dotenv(Path(__file__).with_name(".env"), override=True)
```

This means the examples do not depend on the parent/global `.env` file. A virtual environment only provides installed packages; it does not provide Azure OpenAI settings.

## 1. Create A Model Client

Syntax:

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown",
        "structured_output": False,
    },
)
```

Example:

```python
def create_model_client() -> OpenAIChatCompletionClient:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        model_info={"vision": False, "function_calling": True, "json_output": False, "family": "unknown", "structured_output": False},
    )
```

## 2. Create A Single Agent

Syntax:

```python
from autogen_agentchat.agents import AssistantAgent

agent = AssistantAgent(
    name="agent_name",
    model_client=model_client,
    system_message="Agent instructions.",
)
```

Example:

```python
agent = AssistantAgent(
    name="basic_autogen_agent",
    model_client=model_client,
    system_message="You are a concise beginner-friendly assistant.",
)
```

## 3. Run An Agent

Syntax:

```python
result = await agent.run(task="user task")
print(result.messages[-1].content)
```

Example:

```python
result = await agent.run(task="Explain AutoGen in one paragraph.")
print(result.messages[-1].content)
```

## 4. Tool Calling

Syntax:

```python
def tool_name(input_value: str) -> str:
    return "tool result"

agent = AssistantAgent(
    name="tool_agent",
    model_client=model_client,
    tools=[tool_name],
    max_tool_iterations=3,
    system_message="Use tools when needed.",
)
```

Example:

```python
def calculator(expression: str) -> str:
    return str(eval(expression, {"__builtins__": {}}, {}))

agent = AssistantAgent(
    name="tool_autogen_agent",
    model_client=model_client,
    tools=[calculator, get_weather],
    max_tool_iterations=3,
    system_message="Use tools for math and weather questions.",
)
```

## 5. Multi-Agent Orchestration

Syntax:

```python
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat

team = RoundRobinGroupChat(
    [agent_one, agent_two, agent_three],
    termination_condition=MaxMessageTermination(4),
)
result = await team.run(task="team task")
```

Example:

```python
planner = AssistantAgent("planner", model_client=model_client, system_message="Create a short plan.")
executor = AssistantAgent("executor", model_client=model_client, system_message="Turn the plan into action steps.")
reviewer = AssistantAgent("reviewer", model_client=model_client, system_message="Review risks and missing approvals.")

team = RoundRobinGroupChat(
    [planner, executor, reviewer],
    termination_condition=MaxMessageTermination(4),
)
result = await team.run(task="Design a customer support automation workflow.")
```
