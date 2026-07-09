# OpenAI Agents SDK Hands-on Labs

This repository contains hands-on labs for building agentic AI applications with the OpenAI Agents SDK and Azure AI Foundry / Azure OpenAI.

## Labs

### Module 1: Advanced Agentic AI Architecture Patterns

1. `Enterprise-Agent-Lab`
   - Enterprise tool-calling agent
   - Tools: calculator, date/time, weather, web search

2. `Stateful-Agent-Lab`
   - Stateful agent workflow
   - Short-term conversation memory using `Memory.py`

3. `Planning-Execution-Lab`
   - AI planning and execution pipeline
   - Planner, executor, reviewer agents

### Module 2: Multi-Agent Orchestration Patterns

4. `MultiAgent-Planner-Executor-Reviewer-Lab`
   - Sequential orchestration
   - Planner Agent -> Executor Agent -> Reviewer Agent
   - Includes human approval gate

5. `MultiAgent-Collaboration-Lab`
   - Concurrent orchestration
   - Business, Technical, and Risk agents collaborate
   - Coordinator agent combines results

6. `MultiAgent-Dynamic-Routing-Lab`
   - Supervisor/router architecture
   - Router agent selects the correct specialist agent

## Setup

Create and activate a virtual environment from the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Each lab also has its own `requirements.txt`.

## Environment Files

Real `.env` files are ignored by git.

For each lab:

1. Copy `.env.example` to `.env`.
2. Fill in your Azure AI Foundry / Azure OpenAI values.

Example:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_API_VERSION=2025-08-07
AZURE_OPENAI_DEPLOYMENT=gpt-5
```

## Run A Lab

From the repository root:

```bash
cd Enterprise-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

Use the same pattern for other labs:

```bash
cd Stateful-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd Planning-Execution-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd MultiAgent-Planner-Executor-Reviewer-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd MultiAgent-Collaboration-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd MultiAgent-Dynamic-Routing-Lab
..\.venv\Scripts\python.exe main.py
```

## Notes

- Do not commit real `.env` files.
- Use `.env.example` files for sharing configuration templates.
- `ARCHITECTURE.md` files explain each lab design.
