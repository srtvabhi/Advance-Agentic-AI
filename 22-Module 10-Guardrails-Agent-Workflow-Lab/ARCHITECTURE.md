# Guardrails Agent Workflow Lab Architecture

## Objective

Implement guardrails in an AI agent workflow using LangGraph.

This lab shows how an enterprise AI workflow can inspect a user request before sending it to the model.

## Architecture Flow

```text
User Request
   |
   v
Input Guardrail Node
   |
   +--> Safe Agent Node
   |
   +--> Blocked Response Node
   |
   +--> Human Review Response Node
   |
   v
Audit Node
   |
   v
Final Explanation Node
```

## Folder Structure

```text
22-Module 10-Guardrails-Agent-Workflow-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── graphs/
│   └── guardrail_graph.py
├── nodes/
│   └── guardrail_nodes.py
├── services/
│   ├── guardrail_service.py
│   └── llm_service.py
└── models/
    └── guardrail_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: build_guardrail_graph()
|   from graphs/guardrail_graph.py
|
|-- function: main()
    |
    |-- reads user request
    |-- calls: build_guardrail_graph()
    |-- calls: app.invoke(initial GuardrailState)
    |
    |-- LangGraph starts at input_guardrail_node()
        |
        |-- input_guardrail_node()
        |   |-- calls: classify_request()
        |   |-- calls: build_safe_prompt()
        |   |   from services/guardrail_service.py
        |   |-- writes classification, risk_reason, safe_prompt
        |
        |-- route_after_guardrail()
        |   |
        |   |-- safe -> safe_agent_node()
        |   |-- blocked -> blocked_response_node()
        |   |-- review -> review_response_node()
        |
        |-- safe_agent_node()
        |   |-- calls: ask_model()
        |   |-- writes agent_answer
        |
        |-- blocked_response_node()
        |   |-- writes controlled refusal
        |
        |-- review_response_node()
        |   |-- writes human-review response
        |
        |-- audit_node()
        |   |-- writes audit_record
        |
        |-- final_node()
            |-- writes final_output
```

## Key Learning Points

- Pre-model input guardrails
- Prompt injection detection
- Privacy and secret protection
- Conditional routing in LangGraph
- Auditability and traceability

## How To Run

```bash
cd "22-Module 10-Guardrails-Agent-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```
