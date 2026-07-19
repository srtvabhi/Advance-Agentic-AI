# Lab 7: LangGraph Multi-Step Orchestration Architecture

## Objective

Build a multi-step LangGraph orchestration system.

## Problem Statement

Design an enterprise IT service desk workflow that classifies tickets, routes incidents, escalates urgent issues, and creates a final resolution summary.

## Architecture Flow

```text
User Problem
   |
   v
Intake Node
   |
   v
Planning Node
   |
   v
Execution Node
   |
   v
Summary Node
   |
   v
Final Workflow Output
```

## Folder Structure

```text
7-LangGraph-MultiStep-Orchestration-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── graph/
│   └── orchestration_graph.py
├── nodes/
│   ├── intake_node.py
│   ├── planning_node.py
│   ├── execution_node.py
│   └── summary_node.py
├── services/
│   └── llm_service.py
└── models/
    └── state_models.py
```

## Key Learning Points

- Graph-based orchestration
- Multi-step node design
- State passed between nodes
- Enterprise workflow decomposition
- LangGraph `StateGraph`, `START`, and `END`

## Example Prompts

Use prompts that require multiple workflow stages so learners can see how state moves from one LangGraph node to the next.

```text
Design an enterprise IT service desk workflow that classifies tickets, routes incidents, escalates urgent issues, and creates a final resolution summary.
```

```text
Create a workflow to onboard a new enterprise customer into a SaaS platform, including account setup, security review, integration planning, testing, and handover.
```

```text
Design a workflow for handling a production application outage, including incident intake, severity classification, escalation, recovery steps, and final post-incident summary.
```

```text
Create a multi-step workflow for processing vendor onboarding requests, including document collection, compliance review, approval routing, system setup, and final confirmation.
```

```text
Design a workflow for employee laptop replacement, including request intake, eligibility check, inventory validation, approval, shipping, and closure summary.
```

## How To Run

```bash
cd 7-LangGraph-MultiStep-Orchestration-Lab
..\.venv\Scripts\python.exe main.py
```
