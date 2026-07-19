# Token And Latency Monitoring Lab Architecture

## Objective

Monitor token usage and latency in an AI workflow using LangGraph and optional LangSmith tracing.

This lab captures local telemetry from Azure OpenAI responses and can also send traces to LangSmith when students add their own LangSmith key.

## Problem Statement

Run the lab scenario and observe how the workflow components collaborate to produce the final result.

## Architecture Flow

```text
Business Request
   |
   v
Draft Response Node
   |
   v
Review Response Node
   |
   v
Telemetry Summary Node
   |
   v
Final Report Node
```

## Folder Structure

```text
26-Module 11-Token-Latency-Monitoring-Lab/
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
│   └── monitoring_graph.py
├── models
│   ├── __init__.py
│   └── monitoring_models.py
├── nodes
│   ├── __init__.py
│   └── monitoring_nodes.py
└── services
    ├── __init__.py
    ├── llm_service.py
    └── telemetry_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: configure_langsmith from config.settings
|-- imports: build_monitoring_graph from graphs.monitoring_graph
|-- function: main()
|-- graphs/monitoring_graph.py
|   |-- build_monitoring_graph()
|-- services/llm_service.py
|   |-- ask_model_with_metrics()
|-- services/telemetry_service.py
|   |-- summarize_telemetry()
|-- nodes/monitoring_nodes.py
|   |-- draft_response_node()
|   |-- review_response_node()
|   |-- telemetry_summary_node()
|   |-- final_report_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/monitoring_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/monitoring_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/monitoring_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.
- `services/telemetry_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. Write a short customer update explaining a delay in insurance claim processing.
2. Draft and review a status update for a delayed payroll ticket.
3. Create a customer-facing outage update and monitor token and latency usage.
4. Generate a short executive update for an IT incident and summarize telemetry.
5. Write and review a vendor delay notification while tracking model metrics.

## How To Run

```bash
cd "26-Module 11-Token-Latency-Monitoring-Lab"
..\.venv\Scripts\python.exe main.py
```
