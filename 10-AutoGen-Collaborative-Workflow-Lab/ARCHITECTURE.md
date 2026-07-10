# Lab 10: AutoGen Collaborative Multi-Agent Workflow

## Objective

Build an AutoGen collaborative multi-agent workflow.

## Problem Statement

Design a collaborative AutoGen solution for enterprise loan application processing.

## Architecture Flow

```text
User Task
   |
   v
RoundRobinGroupChat
   |
   +--> Business Analyst Agent
   +--> Solution Architect Agent
   +--> Security Reviewer Agent
   +--> Coordinator Agent
   |
   v
Final Group Recommendation
```

## Folder Structure

```text
10-AutoGen-Collaborative-Workflow-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
├── agents/
├── orchestration/
├── services/
└── models/
```

## Key Learning Points

- AutoGen assistant agents
- Group conversation orchestration
- Enterprise collaboration workflow
- Coordinator/synthesizer agent pattern

## How To Run

```bash
cd 10-AutoGen-Collaborative-Workflow-Lab
..\.venv\Scripts\python.exe main.py
```

