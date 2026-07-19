# Agent Workflow Tracing Lab Architecture

## Objective

Trace an AI agent workflow execution using LangGraph and LangSmith.

LangSmith has a free Developer plan for individual builders, and it can trace workflows that call Azure OpenAI because tracing observes your Python functions and model calls.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Incident Input
   |
   v
Triage Node
   |
   v
Investigation Node
   |
   v
Resolution Node
   |
   v
Trace Notes Node
   |
   v
Final Report Node
```

## Folder Structure

```text
25-Module 11-Agent-Workflow-Tracing-Lab/
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
│   └── tracing_graph.py
├── models
│   ├── __init__.py
│   └── tracing_models.py
├── nodes
│   ├── __init__.py
│   └── tracing_nodes.py
└── services
    ├── __init__.py
    └── llm_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_tracing_graph from graphs.tracing_graph
|-- function: main()
|-- graphs/tracing_graph.py
|   |-- build_tracing_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- nodes/tracing_nodes.py
|   |-- triage_node()
|   |-- investigation_node()
|   |-- resolution_node()
|   |-- trace_notes_node()
|   |-- final_report_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/tracing_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/tracing_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/tracing_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.

## Test Prompts

Use these prompts to test the lab objective:

1. The enterprise HR chatbot is returning slow answers for payroll questions. Support tickets increased by 40 percent in the last hour.
2. Trace an incident where the IT support workflow gives inconsistent VPN troubleshooting answers.
3. Trace a customer service workflow where refund responses are delayed.
4. Trace an invoice approval question workflow that is timing out.
5. Trace a multi-step HR case workflow from triage to resolution message.

## How To Run

```bash
cd "25-Module 11-Agent-Workflow-Tracing-Lab"
..\.venv\Scripts\python.exe main.py
```
