# Multi-Agent Collaboration Lab Architecture

## Objective

Create a multi-agent collaboration pipeline using the OpenAI Agents SDK.

This lab demonstrates concurrent orchestration:

1. Business Agent analyzes business value.
2. Technical Agent analyzes architecture.
3. Risk Agent analyzes governance and risk.
4. Coordinator Agent combines all outputs.

## Architecture Flow

```text
User Scenario
   |
   v
main.py
   |
   +--> Business Agent
   |
   +--> Technical Agent
   |
   +--> Risk Agent
   |
   v
Coordinator Agent
   |
   v
Final Collaboration Summary
```

## Folder Structure

```text
5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab/
├── .env
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── agent/
│   ├── business_agent.py
│   ├── technical_agent.py
│   ├── risk_agent.py
│   └── coordinator_agent.py
└── models/
    └── collaboration_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_openai_client()
|   from config/settings.py
|
|-- imports specialist agent factories:
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
|   |-- create_coordinator_agent()
|       from agent/coordinator_agent.py
|
|-- function: main()
|   |
|   |-- calls: configure_openai_client()
|   |-- creates business, technical, risk, and coordinator agents
|   |-- reads user scenario
|   |
|   |-- starts three specialist tasks at the same time:
|   |   |
|   |   |-- Runner.run(business_agent, scenario)
|   |   |-- Runner.run(technical_agent, scenario)
|   |   |-- Runner.run(risk_agent, scenario)
|   |
|   |-- calls: asyncio.gather()
|   |   |
|   |   |-- waits for all specialist outputs
|   |
|   |-- builds coordinator_prompt using:
|   |   |
|   |   |-- business_result.final_output
|   |   |-- technical_result.final_output
|   |   |-- risk_result.final_output
|   |
|   |-- calls: Runner.run(coordinator_agent, coordinator_prompt)
|   |
|   |-- creates: CollaborationResult()
|       from models/collaboration_models.py
|
|-- prints final collaboration summary
```

## File Responsibilities

- `main.py` runs the concurrent orchestration.
- `business_agent.py` analyzes goals, users, metrics, and adoption.
- `technical_agent.py` analyzes systems, APIs, data, and tools.
- `risk_agent.py` analyzes security, privacy, compliance, and quality risks.
- `coordinator_agent.py` merges specialist outputs into one recommendation.
- `collaboration_models.py` stores the final collaboration result.
- `settings.py` loads the local `.env` and configures the OpenAI client.

## How To Run

```bash
cd 5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab
..\.venv\Scripts\python.exe main.py
```

## Example Prompts

Use prompts that need business, technical, and risk perspectives. This helps learners see why multiple specialist agents are useful.

```text
Our company receives 2,000 IT support tickets every week. Design a multi-agent solution to classify tickets, suggest resolutions, escalate high-priority issues, and reduce average resolution time.
```

```text
A bank wants to automate loan application review. Design a multi-agent workflow where agents analyze customer eligibility, document completeness, fraud risk, and final recommendation.
```

```text
A hospital wants to create an AI assistant for patient appointment scheduling. Design a multi-agent solution that handles patient requests, doctor availability, compliance risks, and escalation to staff.
```

```text
An ecommerce company has many refund and return requests. Design a multi-agent system to check order history, refund policy, fraud risk, customer sentiment, and final action recommendation.
```

```text
A manufacturing company wants to monitor supplier delays. Design a multi-agent workflow where agents analyze supplier performance, business impact, technical integration needs, and operational risk.
```

## Key Learning Points

- Concurrent orchestration
- Specialist agent collaboration
- Coordinator/synthesizer pattern
- Multi-agent collaboration for enterprise workflows
- Separation of business, technical, and risk perspectives


