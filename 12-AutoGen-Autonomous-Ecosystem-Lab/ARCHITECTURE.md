# Lab 12: AutoGen Autonomous Task-Solving Ecosystem

## Objective

Create an autonomous task-solving agent ecosystem using AutoGen.

## Problem Statement

Investigate a payment API slowdown, open an incident, notify the team, analyze likely root cause, and prepare an update.

## Architecture Flow

```text
Incident Task
   |
   v
RoundRobinGroupChat
   |
   +--> Operations Agent + Tools
   +--> Root Cause Agent
   +--> Communications Agent
   +--> Incident Manager Agent
   |
   v
Final Incident Action Plan
```

## Key Learning Points

- Tool-enabled collaborative agents
- Autonomous task execution
- Collaborative coding and analysis-style workflow
- Scaling multi-agent conversations with clear roles

## How To Run

```bash
cd 12-AutoGen-Autonomous-Ecosystem-Lab
..\.venv\Scripts\python.exe main.py
```

