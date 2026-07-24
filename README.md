# Advanced Agentic AI Hands-on Labs

This repository contains hands-on labs for building enterprise agentic AI applications using OpenAI Agents SDK, LangGraph, AutoGen, Semantic Kernel, ChromaDB, Azure AI Foundry / Azure OpenAI, and LangSmith.

Each lab is organized as an enterprise-style project with its own folder, local `.env`, `requirements.txt`, `ARCHITECTURE.md`, and `Reference.md`.

## Labs

### Module 1: Advanced Agentic AI Architecture Patterns

1. `1- OpenAI Agent SDK-Enterprise-Agent-Lab`
2. `2- OpenAI Agent SDK-Stateful-Agent-Lab`
3. `3- OpenAI Agent SDK-Planning-Execution-Lab`

### Module 2: Multi-Agent Orchestration Patterns

4. `4- OpenAI Agent SDK-MultiAgent-Planner-Executor-Reviewer-Lab`
5. `5- OpenAI Agent SDK-MultiAgent-Collaboration-Lab`
6. `6- OpenAI Agent SDK-MultiAgent-Dynamic-Routing-Lab`

### Module 3: LangGraph for Advanced Agent Workflows

7. `7-LangGraph-MultiStep-Orchestration-Lab`
8. `8-LangGraph-Conditional-Routing-Lab`
9. `9-LangGraph-Resilient-Retry-Lab`

### Module 4: AutoGen and Enterprise Agent Collaboration

10. `10-AutoGen-Collaborative-Workflow-Lab`
11. `11-AutoGen-Reviewer-Validation-Lab`
12. `12-AutoGen-Autonomous-Ecosystem-Lab`

### Module 5: Advanced Retrieval-Augmented Generation

13. `13-OpenAI-Agentic-RAG-Lab`
14. `14-OpenAI-Query-Decomposition-RAG-Lab`
15. `15-OpenAI-Hybrid-Search-RAG-Lab`

### Module 8: Semantic Kernel and Enterprise AI Plugins

16. `16-SemanticKernel-Plugins-RAG-Lab`
17. `17-SemanticKernel-Orchestrated-Workflow-Lab`
18. `18-SemanticKernel-Automation-Pipeline-Lab`

### Module 9: Production-Grade AI Agent Design Patterns

19. `19-Module 9-Production-Ready-AI-Workflow-Architecture-Lab`

### Module 10: AI Guardrails, Safety, and Governance

19-A. `19-A-Module 10-Secure-Procurement-Guardrails-Lab`

Labs 20-30 are kept locally and are ignored from GitHub tracking.

## Lab Summaries

### Lab 1: Enterprise Tool-Calling Agent

This lab builds an enterprise-style assistant using the OpenAI Agents SDK. The agent can answer normal questions and call tools for calculator, current date/time, OpenWeatherMap weather, and Serper web search.

The objective is to design an enterprise-grade agent architecture. Learners see how `main.py`, `config`, `agent`, `tools`, `services`, and `models` work together instead of keeping all logic in one file.

Flow: user question -> enterprise agent -> selected tool -> service/API logic -> final response. This teaches separation of concerns, external API integration, tool calling, and maintainable enterprise project structure.

### Lab 2: Stateful Agent Workflow

This lab builds a stateful assistant that remembers earlier messages during the same running session. `Memory.py` stores the conversation history and passes it back to the agent on every turn.

The objective is to build a stateful agent workflow design. Learners understand why a normal stateless prompt forgets earlier details and how short-term memory supports follow-up questions.

Flow: user message -> memory stores message -> agent receives previous context -> agent responds -> memory updates again. This teaches session memory, conversation continuity, memory inspection, and memory clearing.

### Lab 3: Planning and Execution Pipeline

This lab creates an AI planning and execution pipeline using the OpenAI Agents SDK. A planner creates a structured plan, an executor converts the plan into actions, and a reviewer checks the final output.

The objective is to create an AI planning and execution pipeline. Learners see how enterprise work can be decomposed into planning, execution, and review instead of depending on one large response.

Flow: problem statement -> planner -> executor -> approval/status tools -> reviewer -> final pipeline summary. This teaches decomposition, tool-assisted execution, review gates, and workflow quality control.

### Lab 4: Planner, Executor, Reviewer with Human Approval

This lab builds a multi-agent planner-executor-reviewer workflow with human approval checks. The planner designs the work, the executor attempts controlled execution, and the reviewer validates safety and completeness.

The objective is to build a planner-executor-reviewer workflow. Learners see how multi-agent orchestration supports enterprise governance, especially when tasks include sensitive actions.

Flow: enterprise request -> planner -> executor -> approval tool -> reviewer -> final recommendation. This teaches human-in-the-loop checkpoints, approval-aware execution, and risk-based workflow design.

### Lab 5: Multi-Agent Collaboration Pipeline

This lab creates a collaboration pipeline where specialist agents analyze the same business problem from different angles. Business, technical, and risk agents each contribute their own view.

The objective is to create a multi-agent collaboration pipeline. Learners understand that enterprise design often needs multiple perspectives before a final recommendation is useful.

Flow: business problem -> business agent + technical agent + risk agent -> coordinator -> combined solution. This teaches role-based collaboration, synthesis, and enterprise decision support.

### Lab 6: Dynamic Routing Between Specialists

This lab implements dynamic routing between specialist agents. A router decides whether a request should go to a business, technical, risk, or general specialist.

The objective is to implement dynamic routing between multiple agents. Learners see how routing improves relevance, reduces unnecessary agent calls, and supports scalable enterprise assistants.

Flow: user question -> router -> selected specialist -> final answer. This teaches supervisor-style routing, specialist selection, cost-aware orchestration, and targeted responses.

### Lab 7: LangGraph Multi-Step Orchestration

This lab introduces LangGraph as a graph-based workflow engine. The application is modeled as connected nodes instead of one long function.

The objective is to build a multi-step LangGraph orchestration system. Learners understand how state moves from node to node and why graph structure makes workflow behavior easier to inspect.

Flow: user task -> intake node -> planning node -> execution node -> summary node. This teaches graph orchestration, state passing, node design, and explicit workflow control.

### Lab 8: LangGraph Conditional Routing

This lab demonstrates conditional routing in LangGraph. The graph classifies the request and sends it to the right branch.

The objective is to create conditional agent routing flows. Learners see that different business requests should follow different paths based on intent and risk.

Flow: user request -> router node -> business/technical/risk/general branch -> final answer. This teaches conditional edges, branch selection, routing functions, and category-specific handling.

### Lab 9: LangGraph Resilient Retry Workflow

This lab builds a resilient invoice-processing workflow with validation, retry, and controlled failure handling. It checks required invoice fields, verifies vendor status, and retries a simulated temporary vendor API failure.

The objective is to develop a resilient multi-agent workflow with retries. Learners see when a workflow should stop, when it should retry, and when it should continue.

Flow: invoice input -> field extraction -> validation -> vendor verification -> retry if temporary failure -> approval recommendation. This teaches failure handling, retry limits, conditional recovery, and production reliability.

### Lab 10: AutoGen Collaborative Workflow

This lab uses AutoGen to build a collaborative group conversation. Business analyst, solution architect, security reviewer, and coordinator agents contribute in sequence.

The objective is to build an AutoGen collaborative multi-agent workflow. Learners see how `RoundRobinGroupChat` creates a structured discussion and how `MaxMessageTermination` stops the conversation after a fixed number of messages.

Flow: enterprise task -> business analyst -> solution architect -> security reviewer -> coordinator -> final group output. This teaches group chat orchestration, role-based collaboration, and controlled conversation length.

### Lab 11: Reviewer-Validation Pattern

This lab implements a reviewer-validation pattern using AutoGen. A writer creates a policy draft, a reviewer checks it against a checklist, and the workflow performs one revision cycle when needed.

The objective is to implement a reviewer-validation agent pattern. Learners understand that enterprise AI output should often be reviewed before it is accepted.

Flow: task -> policy writer -> validation reviewer -> revision if required -> final review -> validation result. This teaches quality gates, feedback loops, policy validation, and generation-review separation.

### Lab 12: Autonomous Task-Solving Ecosystem

This lab creates an autonomous incident-response ecosystem using AutoGen. Operations, root cause, communications, and manager agents work together on an enterprise incident.

The objective is to create an autonomous task-solving agent ecosystem. Learners see how multiple agents and tools can coordinate around one business problem without manually running each role.

Flow: incident task -> operations actions -> root cause analysis -> stakeholder communication -> manager summary. This teaches autonomous collaboration, incident response, tool-enabled execution, and coordinated enterprise output.

### Lab 13: Multi-Domain Enterprise RAG

This lab builds a multi-domain enterprise RAG workflow using OpenAI, embeddings, and ChromaDB. HR, Sales, and Marketing data are stored separately so retrieval can be routed by business domain.

The objective is to build a multi-step Agentic RAG workflow. Learners see that enterprise RAG should plan retrieval before answering, especially when data is spread across departments.

Flow: question -> domain selection -> retrieval plan -> ChromaDB search -> grounded answer with citations. This teaches retrieval planning, metadata filtering, embeddings, vector storage, and domain-aware answers.

### Lab 14: Query Decomposition RAG

This lab implements query decomposition for RAG. A complex question is broken into smaller sub-questions before retrieval.

The objective is to implement query decomposition for retrieval. Learners see how multi-part business questions become easier to answer when each part retrieves its own evidence.

Flow: complex question -> decomposed questions -> retrieval per sub-question -> retrieval map -> final answer. This teaches multi-hop retrieval, evidence organization, and grounded synthesis.

### Lab 15: Hybrid Search RAG

This lab creates a hybrid search RAG pipeline for product support. It combines semantic search, keyword search, and metadata filtering over product support PDF content.

The objective is to create a hybrid search-based retrieval pipeline. Learners understand why semantic meaning and exact keywords both matter in support scenarios.

Flow: support question -> product detection -> semantic search + keyword search -> deduped evidence -> grounded support answer. This teaches hybrid retrieval, exact-term matching, product filtering, and support knowledge base design.

### Lab 16: Semantic Kernel Plugins with RAG

This lab builds enterprise-style plugins using Semantic Kernel. An HR policy plugin retrieves policy context and creates a simulated HR ticket.

The objective is to build AI plugins using Semantic Kernel. Learners see how native functions and semantic prompts become reusable business capabilities.

Flow: employee question -> HR policy retrieval -> semantic answer -> HR ticket plugin action. This teaches plugins, native functions, semantic functions, RAG-backed answers, and controlled enterprise actions.

### Lab 17: Semantic Kernel Orchestrated Workflow

This lab creates an orchestrated vendor risk workflow using Semantic Kernel. It classifies a vendor request, retrieves policy controls, generates a risk assessment, and creates an approval task.

The objective is to create an orchestrated AI workflow. Learners see how plugin functions and model reasoning can be chained into a business process.

Flow: vendor request -> classify risk -> retrieve controls -> generate assessment -> create approval task. This teaches workflow sequencing, enterprise plugin orchestration, and risk-review automation.

### Lab 18: Semantic Kernel Automation Pipeline

This lab develops a multi-step IT change automation pipeline using Semantic Kernel. It validates a change request, retrieves change standards, creates an implementation plan, opens a simulated change record, and sends a notification.

The objective is to develop a multi-step AI automation pipeline. Learners see how AI can support structured IT operations while keeping governance visible.

Flow: change request -> validate change -> retrieve standard -> generate plan -> create record -> notify stakeholders. This teaches automation pipelines, native plugins, policy-aware planning, and IT change governance.

### Lab 19: Production-Ready Workflow Architecture

This lab designs a production-ready AI workflow architecture using LangGraph. It turns a business requirement into architecture, deployment, reliability, cost, latency, and readiness recommendations.

The objective is to design a production-ready AI workflow architecture. Learners move beyond prototype thinking and consider what production ownership really requires.

Flow: requirement -> architecture design -> reliability planning -> cost/latency review -> production readiness summary. This teaches scalability, deployment patterns, dependency management, and operational readiness.

### Lab 19-A: Secure Procurement Guardrails Workflow

This lab combines guardrails, governance, retrieval grounding, RBAC, and human approval into one secure procurement workflow. It reviews vendor proposals for privacy exposure, prompt injection, unsafe content, requester authority, policy alignment, and approval requirements.

The objective is to demonstrate practical AI safety and governance in a realistic enterprise process. Learners see that security cannot depend only on the model; deterministic checks, approved policy retrieval, output validation, human checkpoints, and audit records all work together.

Flow: procurement request -> validation -> privacy guardrail -> prompt injection guardrail -> content filter -> RBAC check -> policy retrieval -> grounded risk assessment -> output guardrail -> approval decision -> human approval or finalization. This teaches secure workflow design, responsible AI controls, and auditable decision paths.

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
Embedding_Model=text-embedding-3-large
```

## Run A Lab

From the repository root:

```bash
cd "1- OpenAI Agent SDK-Enterprise-Agent-Lab"
..\.venv\Scripts\python.exe main.py
```

Use the same pattern for any other lab folder:

```bash
cd "13-OpenAI-Agentic-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```

## Notes

- Do not commit real `.env` files.
- Use `.env.example` files for sharing configuration templates.
- `ARCHITECTURE.md` files explain each lab design.
- `Reference.md` files explain important syntax and code behavior.
- Labs 20-30 are available only in the local workspace and are ignored from GitHub tracking.
