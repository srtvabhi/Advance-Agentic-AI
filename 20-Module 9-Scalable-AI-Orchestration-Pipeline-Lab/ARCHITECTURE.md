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
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── pipeline_graph.py
├── nodes/
│   └── pipeline_nodes.py
├── services/
│   ├── llm_service.py
│   └── queue_service.py
└── models/
    └── pipeline_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_pipeline_graph()
|   from graphs/pipeline_graph.py
|
|-- function: main()
    |
    |-- reads pipeline objective
    |-- calls: build_pipeline_graph()
    |-- calls: app.invoke(initial PipelineState)
    |
    |-- LangGraph executes:
        |
        |-- receive_events_node()
        |   |-- calls: load_sample_events()
        |   |-- calls: summarize_events()
        |   |   from services/queue_service.py
        |   |-- writes: events, queue_summary
        |
        |-- routing_node()
        |   |-- reads: objective, queue_summary, events
        |   |-- calls: ask_model()
        |   |-- writes: routing_plan
        |
        |-- worker_pool_node()
        |   |-- reads: routing_plan
        |   |-- calls: ask_model()
        |   |-- writes: worker_pool_plan
        |
        |-- scaling_node()
        |   |-- reads: worker_pool_plan
        |   |-- calls: ask_model()
        |   |-- writes: scaling_plan
        |
        |-- final_report_node()
            |-- combines queue, routing, worker, and scaling outputs
            |-- calls: ask_model()
            |-- writes: final_report
```

## Key Learning Points

- Queue-based AI orchestration
- Event-driven execution pipelines
- Stateless worker pool design
- Back-pressure handling
- Latency and cost optimization
- LangGraph node and edge design

## How To Run

```bash
cd "20-Module 9-Scalable-AI-Orchestration-Pipeline-Lab"
..\.venv\Scripts\python.exe main.py
```

## Why This Is Production Grade

This lab separates orchestration, nodes, services, models, and configuration. That mirrors how enterprise teams design AI systems that need to scale beyond a simple local script.
