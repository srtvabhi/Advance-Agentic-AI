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

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: create_model_client()
|   from config/settings.py
|
|-- imports: create_group_chat()
|   from orchestration/group_chat.py
|
|-- imports: format_team_messages()
|   from services/output_service.py
|
|-- function: main()
|   |
|   |-- reads user task
|   |-- calls: create_model_client()
|   |   |
|   |   |-- config/settings.py
|   |       |
|   |       |-- loads local .env
|   |       |-- creates AutoGen OpenAIChatCompletionClient
|   |
|   |-- calls: create_group_chat(model_client)
|   |   |
|   |   |-- orchestration/group_chat.py
|   |       |
|   |       |-- calls create_business_agent(model_client)
|   |       |-- calls create_architect_agent(model_client)
|   |       |-- calls create_security_agent(model_client)
|   |       |-- calls create_coordinator_agent(model_client)
|   |       |   from agents/team_agents.py
|   |       |
|   |       |-- creates RoundRobinGroupChat()
|   |       |-- uses MaxMessageTermination(5)
|   |
|   |-- calls: team.run(task=task)
|   |   |
|   |   |-- AutoGen runs agents in round-robin order
|   |   |-- each agent adds a message to the group conversation
|   |
|   |-- calls: format_team_messages(result.messages)
|   |   |
|   |   |-- services/output_service.py
|   |       |
|   |       |-- skips ThoughtEvent messages
|   |       |-- maps each message to AgentMessage
|   |           from models/conversation_models.py
|   |
|   |-- prints formatted group conversation
|   |-- closes model_client
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
