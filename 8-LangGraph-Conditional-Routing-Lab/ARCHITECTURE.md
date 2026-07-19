# Lab 8: LangGraph Conditional Routing Architecture

## Objective

Create conditional agent routing flows using LangGraph.

## Architecture Flow

```text
User Question
   |
   v
Router Node
   |
   +--> Business Node
   +--> Technical Node
   +--> Risk Node
   +--> General Node
   |
   v
Final Node
```

## Folder Structure

```text
8-LangGraph-Conditional-Routing-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── Reference.md
├── config/
│   └── settings.py
├── graph/
│   └── routing_graph.py
├── nodes/
│   ├── router_node.py
│   ├── business_node.py
│   ├── technical_node.py
│   ├── risk_node.py
│   ├── general_node.py
│   └── final_node.py
├── services/
│   ├── llm_service.py
│   └── routing_service.py
└── models/
    └── state_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_graph()
|   from graph/routing_graph.py
|
|-- function: main()
|   |
|   |-- reads user question
|   |-- calls: build_graph()
|   |-- calls: app.ainvoke({"question": question})
|   |-- prints result["final_response"]
|
|-- graph/routing_graph.py
    |
    |-- imports: RoutingState
    |   from models/state_models.py
    |
    |-- imports node functions:
    |   |
    |   |-- router_node()
    |   |-- business_node()
    |   |-- technical_node()
    |   |-- risk_node()
    |   |-- general_node()
    |   |-- final_node()
    |
    |-- function: choose_route(state)
    |   |
    |   |-- returns state["route"]
    |
    |-- function: build_graph()
        |
        |-- creates: StateGraph(RoutingState)
        |-- adds router and specialist nodes
        |-- adds edge: START -> router
        |-- adds conditional edges from router:
        |   |
        |   |-- business -> business_node()
        |   |-- technical -> technical_node()
        |   |-- risk -> risk_node()
        |   |-- general -> general_node()
        |
        |-- adds specialist edges -> final_node()
        |-- adds edge: final -> END
        |-- returns graph.compile()
```

Node execution:

```text
router_node()
|
|-- calls: ask_llm()
|-- calls: normalize_route()
|-- returns: {"route": route}

selected specialist node()
|
|-- calls: ask_llm()
|-- returns: {"answer": answer}

final_node()
|
|-- combines state["route"] and state["answer"]
|-- returns: {"final_response": final_response}
```

Every LLM-powered node uses the same shared LLM service:

```text
services/llm_service.py
|
|-- function: ask_llm(system_prompt, user_prompt)
    |
    |-- calls: create_openai_client()
    |   from config/settings.py
    |
    |-- calls: get_model_name()
    |   from config/settings.py
    |
    |-- calls: client.chat.completions.create()
    |-- returns: model response text
```

Configuration is loaded from this lab's local `.env` file:

```text
config/settings.py
|
|-- function: load_environment()
|   |
|   |-- loads local .env file
|
|-- function: create_openai_client()
|   |
|   |-- creates AsyncOpenAI client
|
|-- function: get_model_name()
    |
    |-- returns AZURE_OPENAI_DEPLOYMENT
```

## Key Learning Points

- Conditional branching
- Dynamic routing
- Specialist node design
- Supervisor/router pattern in LangGraph

## Example Prompts

Use prompts that clearly belong to different routes so learners can see conditional routing in action.

```text
How do we measure ROI for an AI-powered HR helpdesk agent?
```

```text
What APIs and data sources are needed to build an enterprise IT support agent?
```

```text
What security controls are required for a payroll automation agent?
```

```text
How should we encourage employees to adopt a new internal AI assistant?
```

```text
Explain what an AI agent is in simple language for a non-technical manager.
```

## How To Run

```bash
cd 8-LangGraph-Conditional-Routing-Lab
..\.venv\Scripts\python.exe main.py
```
