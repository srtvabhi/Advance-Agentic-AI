# Retry And Fallback Strategies Lab Architecture

## Objective

Implement retry and fallback strategies using LangGraph.

This lab demonstrates how production AI workflows can recover from temporary dependency failures and switch to a fallback path when the primary service is unavailable.

## Problem Statement

Create a resilient AI workflow for incident summary generation.

The system should:

- Call a primary AI dependency
- Retry after temporary failure
- Switch to fallback when retry limit is reached
- Keep an error log
- Produce a final reliability report

## Architecture Flow

```text
User Task
   |
   v
Primary Dependency Node
   |
   +--> Retry if temporary failure
   |
   +--> Fallback Node if max retries reached
   |
   v
Final Report Node
```

## Folder Structure

```text
21-Module 9-Retry-and-Fallback-Strategies-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── resiliency_graph.py
├── nodes/
│   └── resiliency_nodes.py
├── services/
│   ├── dependency_service.py
│   └── llm_service.py
└── models/
    └── resiliency_models.py
```

## Conditional Routing

The graph uses conditional edges after the primary dependency node:

- `retry` returns to the primary node
- `fallback` goes to the fallback node
- `final` goes to the final report node

## How To Test Fallback

When running the lab, include this phrase in the task:

```text
force fallback
```

That makes the simulated primary dependency fail on every attempt so participants can observe fallback behavior.

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_resiliency_graph()
|   from graphs/resiliency_graph.py
|
|-- function: main()
    |
    |-- reads production task
    |-- calls: build_resiliency_graph()
    |-- calls: app.invoke(initial ResiliencyState)
    |
    |-- LangGraph starts at primary_node()
        |
        |-- primary_node()
        |   |
        |   |-- increments attempt
        |   |-- calls: call_primary_dependency(task, attempt)
        |   |   from services/dependency_service.py
        |   |
        |   |-- on success:
        |   |   |-- calls: ask_model()
        |   |   |-- writes primary_result and status=primary_success
        |   |
        |   |-- on failure:
        |       |-- appends error_log
        |       |-- writes status=retry_needed or fallback_needed
        |
        |-- route_after_primary()
        |   |
        |   |-- retry -> primary_node()
        |   |-- fallback -> fallback_node()
        |   |-- final -> final_node()
        |
        |-- fallback_node()
        |   |-- calls: ask_model()
        |   |-- writes fallback_result and status=fallback_success
        |
        |-- final_node()
            |-- calls: ask_model()
            |-- writes final_answer
```

## Key Learning Points

- Retry design
- Fallback handling
- Conditional routing in LangGraph
- Circuit breaker style thinking
- AI service dependency management
- Reliability engineering for AI systems

## How To Run

```bash
cd "21-Module 9-Retry-and-Fallback-Strategies-Lab"
..\.venv\Scripts\python.exe main.py
```

## Why This Is Production Grade

Production AI systems must expect dependency failures. This lab shows a simple, readable pattern for retrying temporary failures and using a fallback path when the primary dependency is unavailable.
