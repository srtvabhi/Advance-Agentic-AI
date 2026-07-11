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
