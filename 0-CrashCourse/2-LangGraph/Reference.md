# LangGraph Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
```

## 1. Define Graph State

Syntax:

```python
from typing import TypedDict

class AgentState(TypedDict):
    question: str
    answer: str
```

Example:

```python
class MultiAgentState(TypedDict):
    task: str
    plan: str
    execution: str
    review: str
```

## 2. Create A Node

Syntax:

```python
def node_name(state: AgentState) -> AgentState:
    state["answer"] = "updated value"
    return state
```

Example:

```python
def assistant_node(state: AgentState) -> AgentState:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": state["question"]},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state
```

## 3. Build A Graph

Syntax:

```python
from langgraph.graph import END, StateGraph

graph = StateGraph(AgentState)
graph.add_node("node_name", node_function)
graph.set_entry_point("node_name")
graph.add_edge("node_name", END)
app = graph.compile()
```

Example:

```python
graph = StateGraph(AgentState)
graph.add_node("assistant", assistant_node)
graph.set_entry_point("assistant")
graph.add_edge("assistant", END)
app = graph.compile()
```

## 4. Run A Graph

Syntax:

```python
result = app.invoke(initial_state)
```

Example:

```python
result = build_graph().invoke({"question": question, "answer": ""})
print(result["answer"])
```

## 5. Tool Calling In A Graph

Syntax:

```python
def tool_node(state: ToolState) -> ToolState:
    state["tool_result"] = tool_function(state["question"])
    return state
```

Example:

```python
def tool_node(state: ToolState) -> ToolState:
    if "weather" in state["question"].lower():
        state["tool_result"] = get_weather("Delhi")
    else:
        state["tool_result"] = calculator("40 * 5")
    return state
```

## 6. Multi-Agent Orchestration

Syntax:

```python
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("reviewer", reviewer_node)
graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_edge("reviewer", END)
```

Example:

```python
graph = StateGraph(MultiAgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("reviewer", reviewer_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_edge("reviewer", END)
app = graph.compile()
```
