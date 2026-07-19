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

This lab builds an enterprise-style assistant using the OpenAI Agents SDK. It introduces a clean folder structure with `config`, `agent`, `tools`, `services`, and `models`, so learners see how real projects separate responsibilities. The assistant can call multiple tools: calculator, current date/time, OpenWeatherMap weather, and Serper web search. The objective is to design an enterprise-grade agent architecture where the agent does not do everything itself. Instead, the agent decides when a specific tool should be used, and each tool delegates external API or business logic to a service layer. This lab teaches tool-driven systems, external API integration, configuration handling, and response modeling. It is useful for demonstrating how enterprise agents connect to business capabilities while keeping the code understandable and maintainable.

### Lab 2: Stateful Agent Workflow

This lab builds a stateful workflow using the OpenAI Agents SDK. The focus is short-term memory during a running session. A `Memory.py` file stores previous user and assistant messages, and each new turn sends the conversation history back to the model. This lets the assistant answer follow-up questions without the user repeating context. For example, if the user gives a project name or personal preference, the workflow can remember it later in the same session. The objective is to build a stateful agent workflow design and help learners understand the difference between stateless and stateful behavior. The memory is intentionally simple and in-memory only, so the concept is clear before moving to databases, Redis, vector memory, or long-term storage.

### Lab 3: Planning and Execution Pipeline

This lab creates an AI planning and execution pipeline using the OpenAI Agents SDK. It separates work into three responsibilities: a planner creates a structured plan, an executor turns the plan into practical actions, and a reviewer checks risk, missing steps, approval gaps, and execution quality. The workflow uses tools for approval checks and task status simulation. The objective is to show how enterprise workflows can be decomposed into planning, acting, and reviewing stages instead of relying on one assistant response. Learners practice designing a pipeline where each step has a clear owner and output. This is useful for onboarding workflows, process automation, service requests, and business operations where reliability and review matter.

### Lab 4: Planner, Executor, Reviewer with Human Approval

This lab expands the planner-executor-reviewer pattern into a multi-agent orchestration workflow. The planner breaks a risky enterprise request into steps, the executor attempts to carry out the plan, and the reviewer evaluates whether the output is complete and safe. A human approval gate is included for sensitive actions such as deleting production records or granting elevated access. The objective is to build a planner-executor-reviewer workflow and demonstrate human-in-the-loop control. The lab teaches that enterprise automation should pause when an action requires approval, record that decision, and continue only when approval is granted. This makes the design closer to real governance workflows used in production environments.

### Lab 5: Multi-Agent Collaboration Pipeline

This lab builds a collaboration pipeline where different specialists work on the same business problem. A business agent focuses on value, users, process, and adoption. A technical agent focuses on systems, APIs, data flow, and implementation. A risk agent focuses on security, compliance, privacy, and operational risk. A coordinator combines their outputs into one final recommendation. The objective is to create a multi-agent collaboration pipeline for enterprise workflows. Learners see how multiple viewpoints improve solution quality and reduce blind spots. This lab is valuable for solution design, risk assessment, digital transformation planning, and enterprise architecture discussions where one perspective is not enough.

### Lab 6: Dynamic Routing Between Specialists

This lab implements dynamic routing between multiple specialist agents. A router or supervisor decides which specialist should answer based on the user question. If the question is business-focused, it routes to the business specialist. If it is technical, it routes to the technical specialist. If it involves risk or compliance, it routes to the risk specialist. The objective is to implement dynamic routing between multiple agents. This teaches learners how enterprise assistants can avoid sending every request through every agent. Instead, routing improves relevance, cost, and latency by selecting the right capability for the task. This pattern is common in helpdesks, internal portals, and support automation.

### Lab 7: LangGraph Multi-Step Orchestration

This lab introduces LangGraph as a graph-based workflow engine. Instead of a single function call, the application is modeled as connected nodes. Each node performs one step such as intake, planning, execution, or summary. The graph defines the order of execution and passes state between nodes. The objective is to build a multi-step LangGraph orchestration system. Learners understand how graph-based design makes workflow steps explicit and easier to debug. This lab is a foundation for more advanced routing, retries, state management, and production orchestration. It is useful for enterprise workflows where a request must pass through a predictable sequence before final output.

### Lab 8: LangGraph Conditional Routing

This lab demonstrates conditional routing in LangGraph. The workflow receives a user question, a router node classifies the question, and the graph sends it to the correct branch: business, technical, risk, or general. Each branch produces a specialized response before the final output is returned. The objective is to create conditional agent routing flows. This lab teaches how state and routing functions control graph execution. Learners see that not every request should follow the same path. Conditional routing is important for enterprise systems that handle different categories of work, such as customer support, IT requests, compliance review, and business analysis.

### Lab 9: LangGraph Resilient Retry Workflow

This lab develops a resilient workflow with retries. It processes a vendor invoice, extracts invoice fields, validates required information, verifies the vendor, retries a temporary vendor API failure, and generates an approval recommendation. If required fields such as `Vendor:` or `Amount:` are missing, the workflow stops early. If validation passes and vendor verification fails temporarily, the graph retries the vendor node up to a configured limit. The objective is to develop a resilient multi-agent workflow with retries. Learners see how production systems should handle recoverable failures without retrying forever. This lab teaches validation, conditional routing, retry limits, failure messages, and clean recovery behavior.

### Lab 10: AutoGen Collaborative Workflow

This lab uses AutoGen to build a collaborative group conversation. It creates multiple participants such as business analyst, solution architect, security reviewer, and coordinator. A `RoundRobinGroupChat` lets each participant speak in sequence, and `MaxMessageTermination(5)` stops the discussion after a fixed number of messages. The objective is to build a collaborative multi-agent workflow. Learners see how AutoGen can simulate a structured enterprise design discussion where each role contributes a different perspective. The coordinator then brings the ideas together. This lab is useful for solution planning, business process design, security review, and architecture brainstorming where collaboration matters.

### Lab 11: Reviewer-Validation Pattern

This lab implements a reviewer-validation pattern using AutoGen. One agent writes a policy draft, another agent reviews it, and a validation service checks whether important enterprise concerns are covered. The workflow returns a structured validation result containing the draft, review, and final status. The objective is to implement a reviewer-validation agent pattern. This teaches learners that generated content should often be reviewed before use, especially in enterprise settings. The pattern is useful for policy writing, compliance checks, customer communication review, legal review, and security documentation. It introduces the idea of separating generation from quality control.

### Lab 12: Autonomous Task-Solving Ecosystem

This lab creates an autonomous incident-response ecosystem using AutoGen. It includes operations, root cause, communications, and manager roles. The operations role can use tools to check service health, create an incident ticket, and notify the response team. Other roles analyze cause, prepare communication, and summarize next steps. The objective is to create an autonomous task-solving agent ecosystem. Learners see how multiple roles and tools can coordinate around a live business problem such as payment API failure or customer checkout outage. The lab demonstrates autonomous collaboration, tool-enabled execution, incident handling, and enterprise communication flow.

### Lab 13: Multi-Domain Enterprise RAG

This lab redesigns RAG as a multi-domain enterprise knowledge workflow. The data folder contains HR, Sales, and Marketing sources. HR stores a travel policy PDF, Sales stores pipeline data in CSV format, and Marketing stores active campaign notes. The workflow first decides which data domain is relevant to the question, then retrieves from HR, Sales, Marketing, or all sources using ChromaDB metadata filtering. The objective is to build a multi-step Agentic RAG workflow, not just simple document search. Learners understand retrieval planning, domain routing, embeddings, vector storage, filtered retrieval, and grounded answers with citations. This mirrors real enterprise knowledge environments where information is spread across departments.

### Lab 14: Query Decomposition RAG

This lab implements query decomposition for retrieval. It uses a security incident runbook and handles complex questions with multiple parts. The model breaks the original question into smaller sub-questions, the system retrieves evidence for each sub-question, and then the final answer is synthesized from all retrieved evidence. The output clearly shows `Decomposed Questions`, `Final Answer`, and `Retrieval Map`. The objective is to implement query decomposition for retrieval. Learners see how multi-hop questions can be answered more reliably when the system searches for each sub-topic separately. This is useful for incident response, compliance investigation, legal research, and operational troubleshooting.

### Lab 15: Hybrid Search RAG

This lab creates a hybrid search-based retrieval pipeline for product support. It uses an existing product support PDF and stores product-aware chunks in ChromaDB. The workflow detects whether the question mentions `AnalyticsPro` or `SecurePay`, applies metadata filtering, runs semantic search, runs keyword search, deduplicates the combined results, and generates a grounded support answer. The objective is to create a hybrid search-based retrieval pipeline. Learners understand why semantic search and keyword search complement each other. Semantic search captures meaning, while keyword search catches exact error terms such as `token expired`, `cache mismatch`, `webhook`, and `settlement`. This pattern is valuable for support knowledge bases and troubleshooting workflows.

### Lab 16: Semantic Kernel Plugins with RAG

This lab builds enterprise-style plugins using Semantic Kernel. It creates an HR policy plugin that can search policy context and create an HR ticket. The workflow retrieves relevant hybrid work policy content, uses a prompt function to answer the employee question, and then calls a native plugin function to simulate ticket creation. The objective is to build AI plugins using Semantic Kernel. Learners see how Semantic Kernel separates plugin capabilities from orchestration logic. The lab demonstrates native functions, semantic prompts, RAG-backed answers, and business action simulation. It is useful for enterprise plugin patterns where assistants need to retrieve information and perform controlled actions.

### Lab 17: Semantic Kernel Orchestrated Workflow

This lab creates an orchestrated vendor risk workflow using Semantic Kernel. A vendor request is classified, relevant policy controls are retrieved, a risk assessment is generated, and an approval task is created. The objective is to create an orchestrated AI workflow. Learners see how native plugin functions and prompt-based reasoning can be chained into a clear business process. The scenario is realistic for procurement, third-party risk, security review, and compliance teams. The lab demonstrates how Semantic Kernel can coordinate multiple steps while keeping plugin logic separate from orchestration. It teaches workflow sequencing, risk classification, control retrieval, and approval task generation.

### Lab 18: Semantic Kernel Automation Pipeline

This lab develops a multi-step IT change automation pipeline using Semantic Kernel. It validates the change type, retrieves the relevant change management standard, generates an implementation plan, creates a change record, and sends a notification. The objective is to develop a multi-step AI automation pipeline. Learners see how enterprise automation can combine policy retrieval, planning, record creation, and communication. The workflow is intentionally practical: it includes approvals, implementation steps, rollback planning, validation, and communication. This lab is useful for IT service management, release operations, infrastructure change review, and automated governance workflows.

### Lab 19: Production-Ready Workflow Architecture

This lab focuses on designing a production-ready AI workflow architecture. A LangGraph workflow takes a business requirement and produces architecture, deployment pattern, reliability plan, cost and latency considerations, and final summary. The objective is to design a production-ready AI workflow architecture. Learners practice thinking beyond a prototype. They consider scalability, deployment style, reliability engineering, failure handling, service dependencies, and operational readiness. This lab is important because enterprise systems need more than a working prompt. They need monitoring, ownership, availability planning, security boundaries, and cost-aware design. The output helps learners understand what must be reviewed before moving to production.

### Lab 20: Scalable Orchestration Pipeline

This lab builds a scalable orchestration pipeline with LangGraph. It simulates receiving event batches, routing work, planning a worker pool, creating a scaling strategy, and producing a final report. The objective is to build a scalable AI orchestration pipeline. Learners see how enterprise workloads can be processed through event-driven or queue-based patterns rather than one request at a time. The lab teaches queue concepts, routing, worker pools, scaling decisions, and operational reporting. This is useful for high-volume support tickets, claims processing, onboarding requests, monitoring alerts, or invoice workflows where throughput and reliability matter.

### Lab 21: Retry and Fallback Strategies

This lab implements retry and fallback strategies using LangGraph. The workflow attempts to call a primary dependency, checks whether the attempt succeeded, retries when appropriate, and routes to a fallback path when the primary path fails. The objective is to implement retry and fallback strategies. Learners understand that production workflows must expect dependency failures. The design avoids endless retries and provides a controlled fallback path. This lab teaches recoverability, dependency management, conditional routing, retry limits, and graceful degradation. It is useful for workflows that call external services, knowledge bases, APIs, or model endpoints that may temporarily fail.

### Lab 22: Guardrails Agent Workflow

This lab implements guardrails in an AI workflow. A request is classified before execution. Safe requests continue to response generation, unsafe requests are blocked, and every path creates an audit trail. The workflow also reviews the response before final output. The objective is to implement guardrails in an AI agent workflow. Learners see how safety checks can be placed before and after model interaction. The lab covers prompt injection risks, data privacy concerns, blocked responses, safe prompts, response review, and auditability. This is important for enterprise systems that handle sensitive data or need responsible AI controls.

### Lab 23: Approval Checkpoint Execution

This lab adds approval checkpoints to AI execution. The workflow accepts a user role and requested action, assesses risk, decides whether approval is required, creates an approval ticket for sensitive actions, executes safe actions, and writes an audit record. The objective is to add approval checkpoints to AI execution. Learners see how human approval can be built into workflow design for high-risk operations such as exporting employee records, granting production admin access, or disabling security controls. The lab teaches role-based access control, approval routing, audit records, and safe execution patterns.

### Lab 24: Unsafe Prompt Testing

This lab tests workflows against unsafe prompt scenarios. It loads a built-in test suite, evaluates each prompt, counts blocked and allowed prompts, creates an improvement plan, and generates a final report. The objective is to test AI agents against unsafe prompt scenarios. Learners see how safety can be tested systematically rather than manually guessing. The lab includes scenarios such as hidden instruction requests, data exfiltration, approval bypass, and safe business questions. It teaches prompt injection awareness, content filtering concepts, safety evaluation, governance reporting, and iterative improvement of controls.

### Lab 25: Workflow Tracing

This lab uses LangSmith observability to trace a multi-step workflow. The scenario is an enterprise incident such as a slow HR chatbot. The graph performs triage, investigation, resolution messaging, trace note creation, and final report generation. The objective is to trace an AI workflow execution. Learners see how observability helps debug multi-step systems by showing what happened at each node. The lab demonstrates traceable model calls, workflow visibility, incident analysis, and operational notes. This is important because production teams need to inspect prompts, responses, latency, failures, and decision paths.

### Lab 26: Token and Latency Monitoring

This lab monitors token usage and latency across a workflow. It drafts a business response, reviews that response, captures telemetry for each step, summarizes usage, and produces a monitoring report. The objective is to monitor token usage and latency. Learners see that production systems must measure cost and performance, not just output quality. The lab teaches how to collect response time, token counts, and step-level metrics. This helps teams optimize prompts, reduce cost, detect slow steps, and set operational expectations. The scenario is practical for customer updates, incident communication, and business response workflows.

### Lab 27: RAG Quality Evaluation

This lab evaluates RAG response quality using observability concepts. It retrieves HR policy context, generates an answer, uses an LLM-as-judge step to evaluate grounding and completeness, and produces an observability report. The objective is to evaluate RAG response quality using observability tools. Learners see that retrieval-based systems need quality checks. A RAG answer should be supported by retrieved evidence, not unsupported assumptions. The lab teaches retrieval quality, groundedness, evidence checking, answer evaluation, and reporting. It is useful for policy assistants, HR helpdesks, knowledge portals, and compliance question answering.

### Lab 28: End-to-End Enterprise Solution

This capstone lab builds an end-to-end enterprise agentic AI solution design. A LangGraph workflow takes a business problem and produces requirements, architecture, security and compliance review, observability and governance plan, production readiness review, and final solution summary. The objective is to build an end-to-end enterprise Agentic AI solution. Learners bring together concepts from previous labs: planning, orchestration, retrieval, governance, monitoring, and production readiness. The scenario can cover employee services, insurance claims, finance operations, customer service, or IT incident management. It teaches how to structure a complete enterprise solution rather than isolated components.

### Lab 29: Multi-Agent RAG and Tools Orchestration

This capstone lab combines RAG, tools, and multiple workflow roles. It retrieves policy context, runs enterprise tool simulations such as ticket creation and approval checks, creates a plan, executes the plan, reviews the result, and produces a final answer. The objective is to implement multi-agent orchestration with RAG and tools. Learners see how knowledge retrieval and action execution can work together. The workflow is useful for requests such as laptop provisioning, temporary production access, remote work approval, invoice system access, or customer escalation. It demonstrates practical enterprise orchestration where context, tools, planning, execution, and review all matter.

### Lab 30: Deploy and Evaluate Enterprise Workflow

This capstone lab focuses on deployment and evaluation planning for an enterprise AI workflow. It creates a deployment plan, evaluation plan, readiness scorecard, cost and performance plan, and final report. The objective is to deploy and evaluate an enterprise AI workflow architecture. Learners think like production owners: how will the workflow run, scale, be monitored, be evaluated, and be improved? The lab covers Azure deployment considerations, readiness checks, cost and latency planning, governance, and evaluation strategy. It is the final bridge from hands-on prototype thinking to operational enterprise architecture.

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
