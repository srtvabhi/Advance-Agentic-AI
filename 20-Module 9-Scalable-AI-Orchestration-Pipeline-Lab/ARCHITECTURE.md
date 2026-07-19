# Scalable AI Orchestration Pipeline Lab Architecture

## Objective

Build a scalable AI orchestration pipeline using LangGraph.

This lab demonstrates how production AI systems can process events from a queue, route work to the right worker pool, and apply scaling, latency, and cost controls.

## Problem Statement

Design a scalable AI pipeline for insurance claim intake.

The system should:

- Receive claim events from a queue
- Route high-risk claims differently from normal claims
- Use worker pools for distributed processing
- Handle queue back-pressure
- Optimize cost and latency

## Architecture Flow

```text
User Objective
   |
   v
Receive Events Node
   |
   v
Routing Node
   |
   v
Worker Pool Node
   |
   v
Scaling Node
   |
   v
Final Report Node
```

## Folder Structure

```text
20-Module 9-Scalable-AI-Orchestration-Pipeline-Lab/
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
│   └── pipeline_graph.py
├── models
│   ├── __init__.py
│   └── pipeline_models.py
├── nodes
│   ├── __init__.py
│   └── pipeline_nodes.py
└── services
    ├── __init__.py
    ├── llm_service.py
    └── queue_service.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|-- imports: build_pipeline_graph from graphs.pipeline_graph
|-- function: main()
|-- graphs/pipeline_graph.py
|   |-- build_pipeline_graph()
|-- services/llm_service.py
|   |-- ask_model()
|-- services/queue_service.py
|   |-- load_sample_events()
|   |-- summarize_events()
|-- nodes/pipeline_nodes.py
|   |-- receive_events_node()
|   |-- routing_node()
|   |-- worker_pool_node()
|   |-- scaling_node()
|   |-- final_report_node()
```

## File Responsibilities

- `.env`: Supports setup, configuration, reference, or documentation for the lab.
- `.env.example`: Supports setup, configuration, reference, or documentation for the lab.
- `ARCHITECTURE.md`: Supports setup, configuration, reference, or documentation for the lab.
- `config/__init__.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `config/settings.py`: Loads this lab local .env file and creates model, kernel, client, or tracing configuration.
- `graphs/__init__.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `graphs/pipeline_graph.py`: Builds the orchestration flow and connects agents or LangGraph nodes.
- `main.py`: Entry point that accepts input, runs the workflow, and prints the result.
- `models/__init__.py`: Defines data models or TypedDict state shared across the workflow.
- `models/pipeline_models.py`: Defines data models or TypedDict state shared across the workflow.
- `nodes/__init__.py`: Contains workflow node functions that update state step by step.
- `nodes/pipeline_nodes.py`: Contains workflow node functions that update state step by step.
- `Reference.md`: Supports setup, configuration, reference, or documentation for the lab.
- `requirements.txt`: Supports setup, configuration, reference, or documentation for the lab.
- `services/__init__.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.
- `services/llm_service.py`: Wraps Azure OpenAI model calls used by workflow nodes or agents.
- `services/queue_service.py`: Contains reusable business logic, retrieval, telemetry, output, or external-service simulation.

## Test Prompts

Use these prompts to test the lab objective:

1. Build a scalable orchestration pipeline for 10,000 customer support tickets per day.
2. Design a queue-based AI pipeline for insurance claim events across multiple priority levels.
3. Create a scalable workflow for HR onboarding requests during a large hiring wave.
4. Build an event-driven orchestration pipeline for IT incidents from monitoring alerts.
5. Design a worker-pool pipeline for finance invoice processing with surge handling.

## How To Run

```bash
cd "20-Module 9-Scalable-AI-Orchestration-Pipeline-Lab"
..\.venv\Scripts\python.exe main.py
```
