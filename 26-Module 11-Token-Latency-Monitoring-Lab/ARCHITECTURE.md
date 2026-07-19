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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_langsmith()
|   from config/settings.py
|
|-- imports: build_monitoring_graph()
|   from graphs/monitoring_graph.py
|
|-- function: main()
    |
    |-- calls: configure_langsmith()
    |-- reads business request
    |-- calls: build_monitoring_graph()
    |-- calls: app.invoke(initial MonitoringState)
    |
    |-- LangGraph executes:
        |
        |-- draft_response_node()
        |   |-- calls: ask_model_with_metrics()
        |   |   from services/llm_service.py
        |   |-- writes draft_response
        |   |-- appends telemetry metrics
        |
        |-- review_response_node()
        |   |-- reads draft_response
        |   |-- calls: ask_model_with_metrics()
        |   |-- writes reviewed_response
        |   |-- appends telemetry metrics
        |
        |-- telemetry_summary_node()
        |   |-- calls: summarize_telemetry()
        |   |   from services/telemetry_service.py
        |   |-- writes monitoring_summary
        |
        |-- final_report_node()
            |-- combines request, reviewed response, and telemetry
            |-- writes final_report
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
