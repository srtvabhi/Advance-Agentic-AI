# LangGraph Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
```

## Local Environment

Each Python file in this folder loads configuration from this folder's own `.env` file:

```python
load_dotenv(Path(__file__).with_name(".env"), override=True)
```

This means the examples do not depend on the parent/global `.env` file. A virtual environment only provides installed packages; it does not provide Azure OpenAI settings.

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

## 5. Display A Graph

Syntax:

```python
def show_graph(workflow) -> None:
    print(workflow.get_graph().draw_mermaid())
```

Example:

```python
workflow = build_graph()
show_graph(workflow)
```

This prints Mermaid diagram text. Paste the Mermaid output into:

```text
https://mermaid.live
```

Example graph output:

```text
__start__ --> router
router --> calculator
router --> weather
router --> no_tool
calculator --> answer
weather --> answer
no_tool --> answer
answer --> __end__
```

## 6. Tool Calling With Conditional Branches

Syntax:

```python
def router_node(state: ToolState) -> ToolState:
    if "weather" in state["question"].lower():
        state["route"] = "weather"
    elif "calculate" in state["question"].lower():
        state["route"] = "calculator"
    else:
        state["route"] = "no_tool"
    return state

def choose_tool_branch(state: ToolState) -> str:
    return state["route"]
```

Example:

```python
graph = StateGraph(ToolState)
graph.add_node("router", router_node)
graph.add_node("calculator", calculator_node)
graph.add_node("weather", weather_node)
graph.add_node("no_tool", no_tool_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("router")
graph.add_conditional_edges(
    "router",
    choose_tool_branch,
    {
        "calculator": "calculator",
        "weather": "weather",
        "no_tool": "no_tool",
    },
)
graph.add_edge("calculator", "answer")
graph.add_edge("weather", "answer")
graph.add_edge("no_tool", "answer")
graph.add_edge("answer", END)
workflow = graph.compile()
```

Branch node example:

```python
def calculator_node(state: ToolState) -> ToolState:
    expression = state["question"].lower().replace("calculate", "").strip()
    state["tool_result"] = calculator(expression)
    return state
```

## 7. Multi-Agent Orchestration

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
