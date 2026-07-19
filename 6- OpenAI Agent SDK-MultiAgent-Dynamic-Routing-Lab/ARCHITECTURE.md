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
6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab/
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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_openai_client()
|   from config/settings.py
|
|-- imports agent factory functions:
|   |
|   |-- create_router_agent()
|   |   from agent/router_agent.py
|   |
|   |-- create_business_agent()
|   |   from agent/business_agent.py
|   |
|   |-- create_technical_agent()
|   |   from agent/technical_agent.py
|   |
|   |-- create_risk_agent()
|   |   from agent/risk_agent.py
|   |
|   |-- create_general_agent()
|       from agent/general_agent.py
|
|-- imports: normalize_route()
|   from services/routing_service.py
|
|-- function: select_agent(route, agents_by_route)
|   |
|   |-- returns selected specialist agent
|   |-- falls back to general agent
|
|-- function: main()
|   |
|   |-- calls: configure_openai_client()
|   |-- creates router_agent
|   |-- creates agents_by_route dictionary:
|   |   |
|   |   |-- business -> Business Agent
|   |   |-- technical -> Technical Agent
|   |   |-- risk -> Risk Agent
|   |   |-- general -> General Agent
|   |
|   |-- reads user question in a loop
|   |
|   |-- calls: Runner.run(router_agent, question)
|   |-- calls: normalize_route(route_result.final_output)
|   |-- calls: select_agent(route, agents_by_route)
|   |-- calls: Runner.run(selected_agent, question)
|   |
|   |-- creates: RoutingDecision()
|       from models/routing_models.py
|
|-- prints selected route and final answer
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
cd 6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab
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

