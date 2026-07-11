# Agentic Framework Comparison

This file compares the frameworks used in the crash course and full labs.

## High-Level Comparison

| # | Framework | Best For | Main Style | Crash Course Folder |
|---|---|---|---|---|
| 1 | OpenAI Agents SDK | Simple agent apps, tool calling, handoffs, multi-agent workflows | Agent + Runner | `1-OpenAI-Agents-SDK` |
| 2 | LangGraph | Stateful graph workflows, routing, retries, multi-step orchestration | Graph nodes + edges | `2-LangGraph` |
| 3 | AutoGen | Multi-agent conversations and collaboration | Assistant agents + group chat | `3-AutoGen` |
| 4 | OpenAI SDK | Direct model calls and custom orchestration | API client + messages | `4-OpenAI-SDK` |
| 5 | ChromaDB RAG | Vector search and retrieval pipelines | Embeddings + vector store | `5-ChromaDB-RAG` |
| 6 | Semantic Kernel | Plugins, semantic functions, enterprise workflow orchestration | Kernel + plugins | `6-Semantic-Kernel` |

## Agent Creation Syntax

### OpenAI Agents SDK

Syntax:

```python
Agent(name=..., model=..., instructions=...)
```

Example:

```python
agent = Agent(
    name="Basic Assistant",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions="You are a helpful assistant.",
)
```

### LangGraph

Syntax:

```python
def node_name(state):
    return state

graph = StateGraph(StateSchema)
graph.add_node("node_name", node_name)
```

Example:

```python
def assistant_node(state):
    state["answer"] = ask_model(state["question"])
    return state

graph = StateGraph(AgentState)
graph.add_node("assistant", assistant_node)
```

### AutoGen

Syntax:

```python
AssistantAgent(name=..., model_client=..., system_message=...)
```

Example:

```python
agent = AssistantAgent(
    name="basic_autogen_agent",
    model_client=model_client,
    system_message="You are a helpful assistant.",
)
```

### OpenAI SDK

Syntax:

```python
client.chat.completions.create(model=..., messages=[...])
```

Example:

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question},
    ],
)
```

### ChromaDB RAG

Syntax:

```python
context = retrieve_context(question)
response = client.chat.completions.create(...)
```

Example:

```python
context = retrieve_policy(client, question)
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Answer from context only."},
        {"role": "user", "content": f"Question: {question}\nContext: {context}"},
    ],
)
```

### Semantic Kernel

Syntax:

```python
kernel = Kernel()
kernel.add_service(...)
```

Example:

```python
kernel = Kernel()
kernel.add_service(OpenAIChatCompletion(
    ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    async_client=client,
    service_id="foundry-chat",
))
```

## Tool Calling Syntax

### OpenAI Agents SDK

Syntax:

```python
@function_tool
def tool_name(argument: str) -> str:
    ...
```

Example:

```python
@function_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression."""
    return calculate_expression(expression)
```

### LangGraph

Syntax:

```python
def tool_node(state):
    state["tool_result"] = tool_function(...)
    return state
```

Example:

```python
def tool_node(state):
    if "calculate" in state["question"].lower():
        state["tool_result"] = calculator("40 * 5")
    return state
```

### AutoGen

Syntax:

```python
AssistantAgent(..., tools=[tool_function])
```

Example:

```python
agent = AssistantAgent(
    name="tool_autogen_agent",
    model_client=model_client,
    tools=[calculator, get_weather],
    max_tool_iterations=3,
)
```

### OpenAI SDK

Syntax:

```python
tool_result = tool_function(...)
response = client.chat.completions.create(...)
```

Example:

```python
tool_result = calculator("99 / 3")
response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "Answer using tool result."},
        {"role": "user", "content": f"Tool result: {tool_result}"},
    ],
)
```

### ChromaDB RAG

Syntax:

```python
results = collection.query(...)
```

Example:

```python
results = collection.query(
    query_embeddings=[embed(client, question)],
    n_results=2,
)
context = "\n".join(results["documents"][0])
```

### Semantic Kernel

Syntax:

```python
@kernel_function(name="tool_name", description="...")
def tool_name(...):
    ...
```

Example:

```python
class UtilityPlugin:
    @kernel_function(name="calculator", description="Calculate math.")
    def calculator(self, expression: str) -> str:
        return str(eval(expression, {"__builtins__": {}}, {}))

kernel.add_plugin(UtilityPlugin(), plugin_name="Utility")
```

## Orchestration Syntax

### OpenAI Agents SDK

Syntax:

```python
result = await Runner.run(agent, input_text)
```

Example:

```python
plan = await Runner.run(planner_agent, task)
execution = await Runner.run(executor_agent, plan.final_output)
review = await Runner.run(reviewer_agent, execution.final_output)
```

### LangGraph

Syntax:

```python
graph.add_edge("start_node", "next_node")
app = graph.compile()
```

Example:

```python
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("reviewer", reviewer_node)
graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_edge("reviewer", END)
app = graph.compile()
```

### AutoGen

Syntax:

```python
team = RoundRobinGroupChat([...])
result = await team.run(task=...)
```

Example:

```python
team = RoundRobinGroupChat(
    [planner, executor, reviewer],
    termination_condition=MaxMessageTermination(4),
)
result = await team.run(task="Design a workflow")
```

### OpenAI SDK

Syntax:

```python
output_1 = call_model(...)
output_2 = call_model(..., output_1)
```

Example:

```python
plan = call_agent(client, "planner instructions", task)
execution = call_agent(client, "executor instructions", plan)
review = call_agent(client, "reviewer instructions", execution)
```

### ChromaDB RAG

Syntax:

```python
context = retriever(...)
answer = answerer(..., context)
review = reviewer(..., answer)
```

Example:

```python
context = retriever_agent(client, question)
answer = answer_agent(client, question, context)
review = reviewer_agent(client, answer)
```

### Semantic Kernel

Syntax:

```python
result = await semantic_or_native_function(...)
```

Example:

```python
plan = await planner_agent(kernel, task)
execution = await executor_agent(kernel, plan)
review = await reviewer_agent(kernel, execution)
```

## When To Choose Which Framework

| Use Case | Recommended Framework |
|---|---|
| Beginner-friendly single agent with tools | OpenAI Agents SDK |
| Graph workflow with state, branching, retries | LangGraph |
| Multiple agents collaborating in conversation | AutoGen |
| Maximum control with minimal abstraction | OpenAI SDK |
| Retrieval and vector search | ChromaDB RAG |
| Enterprise plugin architecture and workflow automation | Semantic Kernel |

## Short Summary

| Framework | One-Line Summary |
|---|---|
| OpenAI Agents SDK | Fastest way to build agent apps with tools and orchestration. |
| LangGraph | Best when the workflow is a graph with state and routing. |
| AutoGen | Best for conversational multi-agent collaboration. |
| OpenAI SDK | Best for direct API control and custom patterns. |
| ChromaDB RAG | Best for local vector search and retrieval examples. |
| Semantic Kernel | Best for plugin-style enterprise AI orchestration. |
