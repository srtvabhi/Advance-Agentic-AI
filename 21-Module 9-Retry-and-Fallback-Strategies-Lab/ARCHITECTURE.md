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
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config
│   ├── __init__.py
│   └── settings.py
├── graphs
│   ├── __init__.py
│   └── resiliency_graph.py
├── models
│   ├── __init__.py
│   └── resiliency_models.py
├── nodes
│   ├── __init__.py
│   └── resiliency_nodes.py
└── services
    ├── __init__.py
    ├── dependency_service.py
    └── llm_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: build_resiliency_graph from graphs.resiliency_graph
|-- function: main()
|-- graphs/resiliency_graph.py
|   |-- build_resiliency_graph()
|-- services/dependency_service.py
|   |-- call_primary_dependency()
|-- services/llm_service.py
|   |-- ask_model()
|-- nodes/resiliency_nodes.py
|   |-- primary_node()
|   |-- route_after_primary()
|   |-- fallback_node()
|   |-- final_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/resiliency_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/resiliency_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/resiliency_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/dependency_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.

## Test Prompts

Use these prompts to test the lab objective:

1. Process a payment approval task where the primary dependency may fail and fallback is required.
2. Create a retry and fallback workflow for customer support ticket classification.
3. Design resiliency handling for an invoice validation service with temporary outages.
4. Handle HR policy lookup when the primary knowledge service is unavailable.
5. Create a fallback plan for IT incident summarization when the main model call fails.

## How To Run

```bash
cd "21-Module 9-Retry-and-Fallback-Strategies-Lab"
..\.venv\Scripts\python.exe main.py
```
