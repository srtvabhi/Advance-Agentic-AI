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
