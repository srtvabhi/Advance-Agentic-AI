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
├── config/
├── graph/
├── nodes/
├── services/
└── models/
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

## Key Learning Points

- Conditional branching
- Dynamic routing
- Specialist node design
- Supervisor/router pattern in LangGraph

## How To Run

```bash
cd 8-LangGraph-Conditional-Routing-Lab
..\.venv\Scripts\python.exe main.py
```
