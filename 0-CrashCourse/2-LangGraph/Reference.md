# LangGraph Reference

This folder contains three beginner examples:

1. `1_single_agent.py` - one LangGraph node calls the model.
2. `2_single_agent_with_tools.py` - one graph routes to calculator or weather tool branches.
3. `3_multi_agent.py` - planner, executor, and reviewer nodes work in sequence.

## 1. Install The Packages

The versions used by these examples are defined in `requirements.txt`:

```txt
openai==2.44.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
```

Create a virtual environment, activate it, and install the packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
```

What each package provides:

- `openai` provides the OpenAI client used to connect to Azure OpenAI.
- `python-dotenv` loads settings from the local `.env` file.
- `langgraph` provides `StateGraph`, graph nodes, edges, and workflow execution.
- `langchain-core` provides core graph drawing and runnable utilities used by LangGraph.

Activating a virtual environment does not load Azure settings. It only selects the Python interpreter and installed packages.

## 2. Configure The `.env` File

Each Python file in this folder loads configuration from this folder's own `.env` file:

```python
load_dotenv(Path(__file__).with_name(".env"), override=True)
```

Explanation:

- `__file__` is the currently running Python file.
- `Path(__file__)` converts that file path into a path object.
- `.with_name(".env")` points to `.env` in the same folder as the script.
- `override=True` makes sure this local `.env` wins over any parent/global environment value.

The `.env` file needs these values:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-oss-120b
Embedding_Model=text-embedding-3-large
```

The real `.env` file is excluded by `.gitignore`. Use `.env.example` as the template when sharing code on GitHub.

## 3. Common Azure OpenAI Client

All examples create a client like this:

```python
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
```

Explanation:

- `create_client()` groups environment loading and client creation in one place.
- `base_url` sends requests to the Azure OpenAI v1 endpoint.
- `api_key` authenticates with the Azure OpenAI resource.
- `os.environ["AZURE_OPENAI_DEPLOYMENT"]` is later used as the model/deployment name.

## 4. Example 1: Single Agent Graph

File: `1_single_agent.py`

This example has one graph node:

```text
__start__ -> assistant -> __end__
```

### State

```python
class AgentState(TypedDict):
    question: str
    answer: str
```

Explanation:

- `TypedDict` defines the shape of the graph state.
- `question` stores the user input.
- `answer` stores the model response.
- Each node receives this state and returns the updated state.

### Assistant Node

```python
def assistant_node(state: AgentState) -> AgentState:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are a concise beginner-friendly assistant."},
            {"role": "user", "content": state["question"]},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state
```

Explanation:

- The node receives the current graph state.
- It calls Azure OpenAI using the question from `state["question"]`.
- It writes the model response into `state["answer"]`.
- It returns the updated state to LangGraph.

### Build The Graph

```python
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("assistant", assistant_node)
    graph.set_entry_point("assistant")
    graph.add_edge("assistant", END)
    return graph.compile()
```

Explanation:

- `StateGraph(AgentState)` creates a graph whose state follows `AgentState`.
- `add_node("assistant", assistant_node)` registers a node.
- `set_entry_point("assistant")` makes `assistant` the first node.
- `add_edge("assistant", END)` ends the graph after the assistant runs.
- `compile()` converts the graph definition into a runnable workflow.

### Display The Graph

```python
def show_graph(workflow) -> None:
    print("\nLangGraph structure:")
    print(workflow.get_graph().draw_mermaid())
```

Explanation:

- `workflow.get_graph()` gets the compiled graph structure.
- `draw_mermaid()` returns Mermaid diagram text.
- Paste the Mermaid output into `https://mermaid.live` to see a visual chart.

### Run The Graph

```python
workflow = build_graph()
show_graph(workflow)
result = workflow.invoke({"question": question, "answer": ""})
print(result["answer"])
```

Explanation:

- `workflow.invoke(...)` starts the graph.
- The dictionary passed to `invoke` is the initial state.
- The returned `result` is the final state after all nodes finish.

## 5. Example 2: Single Agent With Tool Branches

File: `2_single_agent_with_tools.py`

This example shows conditional branching:

```text
__start__ -> router
router -> calculator
router -> weather
router -> no_tool
calculator -> answer
weather -> answer
no_tool -> answer
answer -> __end__
```

### Tool State

```python
class ToolState(TypedDict):
    question: str
    route: str
    tool_result: str
    answer: str
```

Explanation:

- `question` stores the user request.
- `route` stores the selected branch name.
- `tool_result` stores output from calculator, weather, or no-tool branch.
- `answer` stores the final model explanation.

### Calculator Tool

```python
def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"
```

Explanation:

- The calculator accepts a simple math expression as text.
- `allowed_chars` blocks non-math characters.
- `eval(...)` computes the expression in a restricted context.
- This is acceptable for a small crash-course demo, but production systems should use a proper expression parser.

### Weather Tool

```python
def get_weather(city: str) -> str:
    params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    return f"{data['name']}: {data['weather'][0]['description']}, {data['main']['temp']} C."
```

Explanation:

- `urlencode(...)` safely creates query-string parameters.
- `urlopen(...)` calls the OpenWeather API.
- `json.loads(...)` converts JSON text into a Python dictionary.
- The tool returns a short weather summary.

### Router Node

```python
def router_node(state: ToolState) -> ToolState:
    question = state["question"].lower()
    if "weather" in question:
        state["route"] = "weather"
    elif "calculate" in question:
        state["route"] = "calculator"
    else:
        state["route"] = "no_tool"
    return state
```

Explanation:

- The router is the decision node.
- It reads the user's question and decides which branch should run.
- It writes the branch name into `state["route"]`.

### Conditional Edge Function

```python
def choose_tool_branch(state: ToolState) -> str:
    return state["route"]
```

Explanation:

- LangGraph calls this function after the router node.
- The returned string must match one of the branch names in `add_conditional_edges`.

### Branch Nodes

```python
def calculator_node(state: ToolState) -> ToolState:
    expression = state["question"].lower().replace("calculate", "").strip()
    state["tool_result"] = calculator(expression)
    return state
```

```python
def weather_node(state: ToolState) -> ToolState:
    question = state["question"].lower()
    city = state["question"].split(" in ")[-1].strip(" ?.") if " in " in question else "Delhi"
    state["tool_result"] = get_weather(city)
    return state
```

```python
def no_tool_node(state: ToolState) -> ToolState:
    state["tool_result"] = "No tool needed."
    return state
```

Explanation:

- `calculator_node` calls the calculator function.
- `weather_node` extracts a city name and calls the weather function.
- `no_tool_node` handles questions that do not match calculator or weather.
- All three branches write to the same `tool_result` field.

### Answer Node

```python
def answer_node(state: ToolState) -> ToolState:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Explain the tool result in one short answer."},
            {"role": "user", "content": f"Question: {state['question']}\nTool result: {state['tool_result']}"},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state
```

Explanation:

- The answer node receives the selected tool result.
- It asks the model to convert that raw tool result into a short user-facing answer.

### Build The Conditional Graph

```python
graph.add_conditional_edges(
    "router",
    choose_tool_branch,
    {
        "calculator": "calculator",
        "weather": "weather",
        "no_tool": "no_tool",
    },
)
```

Explanation:

- `router` is the node where branching starts.
- `choose_tool_branch` returns the selected branch name.
- The dictionary maps route names to graph node names.
- Dotted Mermaid arrows show these conditional branches in the graph chart.

Run the example:

```powershell
python 2_single_agent_with_tools.py
```

Example prompts:

```text
Calculate 40 * 5
Calculate 150 / 3 + 20
What is the weather in Delhi?
Get weather in London
```

## 6. Example 3: Multi-Agent Orchestration

File: `3_multi_agent.py`

This example uses three node-based agents:

1. Planner node - creates a plan.
2. Executor node - turns the plan into actions.
3. Reviewer node - checks risks and approvals.

Graph flow:

```text
__start__ -> planner -> executor -> reviewer -> __end__
```

### Multi-Agent State

```python
class MultiAgentState(TypedDict):
    task: str
    plan: str
    execution: str
    review: str
```

Explanation:

- `task` stores the original user request.
- `plan` stores the Planner output.
- `execution` stores the Executor output.
- `review` stores the Reviewer output.
- The graph state carries each agent's output to the next agent.

### Shared Model Helper

```python
def ask_model(system_prompt: str, user_prompt: str) -> str:
    client = create_client()
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""
```

Explanation:

- `ask_model` avoids repeating the same OpenAI call in every node.
- `system_prompt` defines the role of the node.
- `user_prompt` contains the input for that role.
- The helper returns plain text from the model.

### Planner Node

```python
def planner_node(state: MultiAgentState) -> MultiAgentState:
    state["plan"] = ask_model("You are a planner. Create 5 short steps.", state["task"])
    return state
```

The Planner receives the original task and creates a short plan.

### Executor Node

```python
def executor_node(state: MultiAgentState) -> MultiAgentState:
    state["execution"] = ask_model("You are an executor. Add owners and actions.", state["plan"])
    return state
```

The Executor receives the Planner output and adds practical actions and owners.

### Reviewer Node

```python
def reviewer_node(state: MultiAgentState) -> MultiAgentState:
    state["review"] = ask_model("You are a reviewer. Find risks and missing approvals.", state["execution"])
    return state
```

The Reviewer receives the Executor output and checks for risks or missing approvals.

### Build The Multi-Agent Graph

```python
graph = StateGraph(MultiAgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("reviewer", reviewer_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_edge("reviewer", END)
workflow = graph.compile()
```

Explanation:

- Each agent is represented as a graph node.
- Edges define the order of collaboration.
- This is sequential multi-agent orchestration.
- LangGraph controls state movement between agents.

Run the example:

```powershell
python 3_multi_agent.py
```

Example tasks:

```text
Plan the migration of 50 applications to Azure within 6 months using a team of 10 engineers.

Create a project plan to reduce production incidents by 25% within 90 days.
```

## 7. Troubleshooting

### `ModuleNotFoundError: No module named 'langgraph'`

Install this folder's requirements:

```powershell
python -m pip install -r requirements.txt
```

### Missing Environment Variable

An error such as `KeyError: 'AZURE_OPENAI_ENDPOINT'` means the local `.env` file is missing or does not contain the required value.

### Graph Does Not Show As A Picture

The code prints Mermaid text, not an image. Paste the Mermaid output into:

```text
https://mermaid.live
```

### ASCII Graph Error

If you use `draw_ascii()` or `print_ascii()`, LangGraph may require:

```powershell
python -m pip install grandalf
```

These examples use `draw_mermaid()` so `grandalf` is not required.

### Weather Tool Failure

Check the OpenWeather API key, city name, internet connection, and API status.
