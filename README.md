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
20. `20-Module 9-Scalable-AI-Orchestration-Pipeline-Lab`
21. `21-Module 9-Retry-and-Fallback-Strategies-Lab`

### Module 10: AI Guardrails, Safety, and Governance

22. `22-Module 10-Guardrails-Agent-Workflow-Lab`
23. `23-Module 10-Approval-Checkpoint-AI-Execution-Lab`
24. `24-Module 10-Unsafe-Prompt-Testing-Lab`

### Module 11: Observability and Monitoring for Agentic AI

25. `25-Module 11-Agent-Workflow-Tracing-Lab`
26. `26-Module 11-Token-Latency-Monitoring-Lab`
27. `27-Module 11-RAG-Quality-Evaluation-Lab`

### Module 12: End-to-End Enterprise Agentic AI Capstone

28. `28-Module 12-End-to-End-Enterprise-Agentic-AI-Solution-Lab`
29. `29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab`
30. `30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab`

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

### Lab 20: Scalable Orchestration Pipeline

This lab builds a scalable orchestration pipeline using LangGraph. It simulates event intake, queue-based processing, worker planning, scaling strategy, and final reporting.

The objective is to build a scalable AI orchestration pipeline. Learners see how high-volume enterprise requests should be handled through controlled execution patterns.

Flow: event batch -> route work -> plan worker pool -> scaling decision -> final operations report. This teaches queue-based orchestration, event-driven design, throughput planning, and scalable workflow operations.

### Lab 21: Retry and Fallback Strategies

This lab implements retry and fallback strategies using LangGraph. It simulates a primary service failure, retries within a limit, and then routes to a fallback path if needed.

The objective is to implement retry and fallback strategies. Learners understand how reliable workflows handle dependency failures without retrying forever.

Flow: request -> primary dependency -> success check -> retry if recoverable -> fallback if failed -> final response. This teaches graceful degradation, retry limits, dependency resilience, and recovery design.

### Lab 22: Guardrails Agent Workflow

This lab implements guardrails in a LangGraph AI workflow. It checks a request before execution, blocks unsafe content, reviews generated output, and records audit details.

The objective is to implement guardrails in an AI agent workflow. Learners see where safety controls should be placed before and after model interaction.

Flow: user request -> guardrail classification -> allow/block path -> response review -> audit record. This teaches prompt injection defense, privacy protection, safety routing, and responsible AI auditability.

### Lab 23: Approval Checkpoint Execution

This lab adds approval checkpoints to AI execution using LangGraph. It evaluates the requested action, checks risk, routes sensitive actions to approval, and records the outcome.

The objective is to add approval checkpoints to AI execution. Learners see how human approval protects high-risk enterprise operations.

Flow: role + action -> risk check -> approval needed? -> approval ticket or direct execution -> audit record. This teaches human approval systems, RBAC thinking, controlled execution, and governance evidence.

### Lab 24: Unsafe Prompt Testing

This lab tests AI workflows against unsafe prompt scenarios. It runs a test suite with safe and unsafe prompts, evaluates the decisions, and produces a governance report.

The objective is to test AI agents against unsafe prompt scenarios. Learners see how safety can be tested systematically instead of relying on manual inspection.

Flow: test prompt suite -> safety evaluation -> blocked/allowed counts -> improvement plan -> final report. This teaches prompt injection testing, unsafe request detection, content governance, and safety regression testing.

### Lab 25: Workflow Tracing

This lab uses LangSmith with LangGraph to trace a multi-step AI workflow. It follows an enterprise incident through triage, investigation, resolution messaging, trace notes, and final reporting.

The objective is to trace an AI agent workflow execution. Learners see how observability helps teams understand what happened at each node.

Flow: incident input -> triage -> investigation -> resolution message -> trace note -> final report. This teaches tracing, workflow visibility, debugging, prompt/response monitoring, and operational transparency.

### Lab 26: Token and Latency Monitoring

This lab monitors token usage and latency across an AI workflow. It drafts a response, reviews it, captures telemetry, summarizes metrics, and creates a monitoring report.

The objective is to monitor token usage and latency. Learners understand that production systems must measure cost and performance as well as answer quality.

Flow: business task -> draft response -> review response -> collect telemetry -> monitoring report. This teaches latency tracking, token accounting, cost awareness, and performance optimization.

### Lab 27: RAG Quality Evaluation

This lab evaluates RAG response quality with observability concepts. It retrieves HR policy context, generates an answer, and uses an LLM-as-judge style step to evaluate grounding and completeness.

The objective is to evaluate RAG response quality using observability tools. Learners see that RAG systems need evidence checks, not just fluent answers.

Flow: question -> retrieve policy context -> generate answer -> judge groundedness -> quality report. This teaches RAG evaluation, groundedness, completeness checks, and evidence-based quality review.

### Lab 28: End-to-End Enterprise Solution

This capstone lab builds an end-to-end enterprise agentic AI solution design. It turns a business problem into requirements, architecture, security review, observability plan, governance plan, and readiness summary.

The objective is to build an end-to-end enterprise Agentic AI solution. Learners bring together planning, orchestration, governance, monitoring, and production readiness.

Flow: business problem -> requirements -> architecture -> security/compliance -> observability/governance -> final solution. This teaches complete enterprise solution design rather than isolated agent examples.

### Lab 29: Multi-Agent RAG and Tools Orchestration

This capstone lab combines multi-agent orchestration, RAG, and tools. It retrieves policy context, creates a plan, runs tool simulations such as ticket creation and approval checks, reviews the result, and produces a final answer.

The objective is to implement multi-agent orchestration with RAG and tools. Learners see how retrieved knowledge and controlled actions work together in enterprise workflows.

Flow: user request -> retrieve context -> plan -> execute tools -> review -> final answer. This teaches policy-grounded execution, tool orchestration, review gates, and enterprise workflow automation.

### Lab 30: Deploy and Evaluate Enterprise Workflow

This capstone lab focuses on deployment and evaluation planning for an enterprise AI workflow. It creates a deployment plan, evaluation plan, readiness scorecard, cost/performance plan, and final report.

The objective is to deploy and evaluate an enterprise AI workflow architecture. Learners think like production owners who must run, monitor, measure, and improve the system.

Flow: workflow design -> deployment plan -> evaluation strategy -> readiness scorecard -> cost/performance review -> final report. This teaches operationalization, Azure deployment planning, evaluation, governance, and production readiness.

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

```bash
cd "30-Module 12-Deploy-Evaluate-Enterprise-AI-Workflow-Lab"
..\.venv\Scripts\python.exe main.py
```

## Notes

- Do not commit real `.env` files.
- Use `.env.example` files for sharing configuration templates.
- `ARCHITECTURE.md` files explain each lab design.
- `Reference.md` files explain important syntax and code behavior.
