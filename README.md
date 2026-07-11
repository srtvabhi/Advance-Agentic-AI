# OpenAI Agents SDK Hands-on Labs

This repository contains hands-on labs for building agentic AI applications with the OpenAI Agents SDK and Azure AI Foundry / Azure OpenAI.

## Labs

### Module 1: Advanced Agentic AI Architecture Patterns

1. `1- OpenAI Agent SDK-Enterprise-Agent-Lab`
   - Enterprise tool-calling agent
   - Tools: calculator, date/time, weather, web search

2. `2- OpenAI Agent SDK-Stateful-Agent-Lab`
   - Stateful agent workflow
   - Short-term conversation memory using `Memory.py`

3. `3- OpenAI Agent SDK-Planning-Execution-Lab`
   - AI planning and execution pipeline
   - Planner, executor, reviewer agents

### Module 2: Multi-Agent Orchestration Patterns

4. `4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab`
   - Sequential orchestration
   - Planner Agent -> Executor Agent -> Reviewer Agent
   - Includes human approval gate

5. `5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab`
   - Concurrent orchestration
   - Business, Technical, and Risk agents collaborate
   - Coordinator agent combines results

6. `6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab`
   - Supervisor/router architecture
   - Router agent selects the correct specialist agent

### Module 3: LangGraph for Advanced Agent Workflows

7. `7-LangGraph-MultiStep-Orchestration-Lab`
   - Multi-step LangGraph orchestration
   - Intake -> planning -> execution -> summary

8. `8-LangGraph-Conditional-Routing-Lab`
   - Conditional agent routing flow
   - Router node selects business, technical, risk, or general node

9. `9-LangGraph-Resilient-Retry-Lab`
   - Resilient workflow with retries
   - Invoice processing with validation, retry, and approval recommendation

### Module 4: AutoGen and Enterprise Agent Collaboration

10. `10-AutoGen-Collaborative-Workflow-Lab`
   - AutoGen collaborative group conversation
   - Business, architecture, security, and coordinator agents

11. `11-AutoGen-Reviewer-Validation-Lab`
   - Reviewer-validation agent pattern
   - Policy writer and validation reviewer agents

12. `12-AutoGen-Autonomous-Ecosystem-Lab`
   - Autonomous task-solving ecosystem
   - Tool-enabled operations agent with incident response agents

### Module 5: Advanced Retrieval-Augmented Generation (RAG)

13. `13-OpenAI-Agentic-RAG-Lab`
   - Multi-step Agentic RAG workflow
   - Retrieval planning, PDF chunking, ChromaDB, and grounded answers

14. `14-OpenAI-Query-Decomposition-RAG-Lab`
   - Query decomposition for retrieval
   - Multi-hop retrieval over a security incident runbook PDF

15. `15-OpenAI-Hybrid-Search-RAG-Lab`
   - Hybrid retrieval pipeline
   - Semantic search, keyword search, metadata filtering, and ChromaDB

### Module 8: Semantic Kernel and Enterprise AI Plugins

16. `16-SemanticKernel-Plugins-RAG-Lab`
   - Build AI plugins using Semantic Kernel
   - HR policy RAG plugin with ChromaDB

17. `17-SemanticKernel-Orchestrated-Workflow-Lab`
   - Orchestrated AI workflow
   - Vendor risk workflow with native plugins and semantic functions

18. `18-SemanticKernel-Automation-Pipeline-Lab`
   - Multi-step AI automation pipeline
   - IT change automation with RAG-backed standards retrieval

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
cd 1- OpenAI Agent SDK-Enterprise-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

Use the same pattern for other labs:

```bash
cd 2- OpenAI Agent SDK-Stateful-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 3- OpenAI Agent SDK-Planning-Execution-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 7-LangGraph-MultiStep-Orchestration-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 8-LangGraph-Conditional-Routing-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 9-LangGraph-Resilient-Retry-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 10-AutoGen-Collaborative-Workflow-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 11-AutoGen-Reviewer-Validation-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 12-AutoGen-Autonomous-Ecosystem-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 13-OpenAI-Agentic-RAG-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 14-OpenAI-Query-Decomposition-RAG-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 15-OpenAI-Hybrid-Search-RAG-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 16-SemanticKernel-Plugins-RAG-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 17-SemanticKernel-Orchestrated-Workflow-Lab
..\.venv\Scripts\python.exe main.py
```

```bash
cd 18-SemanticKernel-Automation-Pipeline-Lab
..\.venv\Scripts\python.exe main.py
```

## Notes

- Do not commit real `.env` files.
- Use `.env.example` files for sharing configuration templates.
- `ARCHITECTURE.md` files explain each lab design.

