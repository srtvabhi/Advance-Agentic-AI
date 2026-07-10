# Lab 8: LangGraph Conditional Routing Architecture

## Objective

Create conditional agent routing flows using LangGraph.

## Architecture Flow

```text
User Question
   |
   v
Router Node
   |
   +--> Business Node
   +--> Technical Node
   +--> Risk Node
   +--> General Node
   |
   v
Final Node
```

## Folder Structure

```text
8-LangGraph-Conditional-Routing-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── config/
├── graph/
├── nodes/
├── services/
└── models/
```

## Key Learning Points

- Conditional branching
- Dynamic routing
- Specialist node design
- Supervisor/router pattern in LangGraph

## How To Run

```bash
cd 8-LangGraph-Conditional-Routing-Lab
..\.venv\Scripts\python.exe main.py
```

