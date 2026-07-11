# Agent Workflow Tracing Lab Architecture

## Objective

Trace an AI agent workflow execution using LangGraph and LangSmith.

LangSmith has a free Developer plan for individual builders, and it can trace workflows that call Azure OpenAI because tracing observes your Python functions and model calls.

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
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── tracing_graph.py
├── nodes/
│   └── tracing_nodes.py
├── services/
│   └── llm_service.py
└── models/
    └── tracing_models.py
```

## LangSmith Setup

Students can create their own LangSmith key and update `.env`:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=module-11-agent-tracing-lab
```

Without a key, the lab still runs locally and prints `LangSmith tracing enabled: False`.

## How To Run

```bash
cd "25-Module 11-Agent-Workflow-Tracing-Lab"
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

- Workflow tracing
- Agent execution tracking
- Debugging node-by-node execution
- Observing model calls
- Using LangSmith with Azure OpenAI model calls
