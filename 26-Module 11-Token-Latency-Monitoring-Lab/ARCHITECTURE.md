# Token And Latency Monitoring Lab Architecture

## Objective

Monitor token usage and latency in an AI workflow using LangGraph and optional LangSmith tracing.

This lab captures local telemetry from Azure OpenAI responses and can also send traces to LangSmith when students add their own LangSmith key.

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
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── monitoring_graph.py
├── nodes/
│   └── monitoring_nodes.py
├── services/
│   ├── llm_service.py
│   └── telemetry_service.py
└── models/
    └── monitoring_models.py
```

## LangSmith Setup

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=module-11-token-latency-lab
```

## What Is Monitored

- Step name
- Prompt tokens
- Completion tokens
- Total tokens
- Latency in milliseconds

## How To Run

```bash
cd "26-Module 11-Token-Latency-Monitoring-Lab"
..\.venv\Scripts\python.exe main.py
```
