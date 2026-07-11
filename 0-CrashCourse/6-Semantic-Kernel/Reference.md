# Semantic Kernel Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
semantic-kernel==1.44.0
```

## 1. Create A Kernel

Syntax:

```python
from semantic_kernel import Kernel

kernel = Kernel()
```

Example:

```python
kernel = Kernel()
```

## 2. Add OpenAI Chat Completion Service

Syntax:

```python
from openai import AsyncOpenAI
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

client = AsyncOpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

kernel.add_service(
    OpenAIChatCompletion(
        ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        async_client=client,
        service_id="foundry-chat",
    )
)
```

Example:

```python
client = AsyncOpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])
kernel.add_service(
    OpenAIChatCompletion(
        ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        async_client=client,
        service_id="foundry-chat",
    )
)
```

## 3. Run A Semantic Function

Syntax:

```python
from semantic_kernel.functions import KernelArguments

result = await kernel.invoke_prompt(
    "Prompt with {{$variable}}",
    arguments=KernelArguments(variable="value"),
)
```

Example:

```python
result = await kernel.invoke_prompt(
    "You are a concise assistant. Answer this question:\n{{$question}}",
    arguments=KernelArguments(question="Explain Semantic Kernel."),
)
```

## 4. Create A Native Tool Plugin

Syntax:

```python
from semantic_kernel.functions import kernel_function

class PluginName:
    @kernel_function(name="tool_name", description="Tool description.")
    def tool_name(self, input_value: str) -> str:
        return "tool result"
```

Example:

```python
class UtilityPlugin:
    @kernel_function(name="calculator", description="Calculate a simple math expression.")
    def calculator(self, expression: str) -> str:
        return str(eval(expression, {"__builtins__": {}}, {}))
```

## 5. Add A Plugin To Kernel

Syntax:

```python
kernel.add_plugin(PluginName(), plugin_name="PluginAlias")
```

Example:

```python
kernel.add_plugin(UtilityPlugin(), plugin_name="Utility")
```

## 6. Invoke A Tool

Syntax:

```python
result = await kernel.invoke(
    plugin_name="PluginAlias",
    function_name="tool_name",
    input_value="value",
)
```

Example:

```python
tool_result = await kernel.invoke(
    plugin_name="Utility",
    function_name="calculator",
    expression="18 * 7",
)
```

## 7. Multi-Agent Orchestration

Syntax:

```python
plan = await planner_agent(kernel, task)
execution = await executor_agent(kernel, plan)
review = await reviewer_agent(kernel, execution)
```

Example:

```python
plan = await planner_agent(kernel, "Create a vendor onboarding workflow.")
execution = await executor_agent(kernel, plan)
review = await reviewer_agent(kernel, execution)
```
