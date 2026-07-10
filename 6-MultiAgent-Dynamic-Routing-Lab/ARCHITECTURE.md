# Dynamic Agent Routing Lab Architecture

## Objective

Implement dynamic routing between multiple agents using the OpenAI Agents SDK.

This lab demonstrates supervisor agent architecture:

1. Router Agent reads the user question.
2. Router Agent chooses the best specialist.
3. The selected specialist answers the question.

## Architecture Flow

```text
User Question
   |
   v
Router Agent
   |
   +--> Business Specialist
   |
   +--> Technical Specialist
   |
   +--> Risk Specialist
   |
   +--> General Specialist
   |
   v
Final Answer
```

## Folder Structure

```text
6-MultiAgent-Dynamic-Routing-Lab/
├── .env
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── agent/
│   ├── router_agent.py
│   ├── business_agent.py
│   ├── technical_agent.py
│   ├── risk_agent.py
│   └── general_agent.py
├── services/
│   └── routing_service.py
└── models/
    └── routing_models.py
```

## File Responsibilities

- `main.py` runs the routing loop.
- `router_agent.py` decides which specialist should answer.
- `business_agent.py` handles business questions.
- `technical_agent.py` handles architecture and implementation questions.
- `risk_agent.py` handles security, compliance, and governance questions.
- `general_agent.py` handles fallback/general questions.
- `routing_service.py` normalizes router output into a stable route.
- `routing_models.py` stores the routing decision and final answer.
- `settings.py` loads the local `.env` and configures the OpenAI client.

## How To Run

```bash
cd 6-MultiAgent-Dynamic-Routing-Lab
..\.venv\Scripts\python.exe main.py
```

## Example Prompts

```text
What APIs are needed for a customer support agent?
```

```text
How do we measure ROI for an HR agent?
```

```text
What security controls are required for payroll access?
```

## Key Learning Points

- Supervisor agent architecture
- Dynamic task routing
- Specialist agents
- Fallback agent pattern
- Multi-agent orchestration for enterprise workflows

