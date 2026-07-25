# Lab 20 Architecture: Observability and Monitoring for Agentic RAG

## Objective

This lab implements observability for an existing Agentic RAG workflow using LangSmith.

The lab objectives are:

- Trace an AI agent workflow execution
- Monitor token usage and latency
- Evaluate RAG response quality using observability tools

## Business Problem

An enterprise has HR, Sales, and Marketing knowledge sources. A business user asks a question, and the Agentic RAG workflow must decide which department knowledge store to use, retrieve relevant evidence, generate a grounded answer, and show whether the answer is reliable.

In production, it is not enough to only show the final answer. Teams need to see:

- Which agent step ran
- Which vector store was searched
- Which chunks were retrieved
- How long each step took
- Approximate token usage
- Whether the answer was grounded in retrieved context

LangSmith provides this visibility by tracing the workflow execution.

## Architecture Flow

```text
User Question
   |
   v
main.py
   |
   v
run_agentic_rag()
   |
   +--> configure_langsmith()
   |
   +--> build_index()
   |       |
   |       +--> HR data --------> vector_store/hr_knowledge
   |       +--> Sales data -----> vector_store/sales_knowledge
   |       +--> Marketing data -> vector_store/marketing_knowledge
   |
   +--> Domain Router Agent
   |       |
   |       +--> LangSmith span: domain_router_agent
   |
   +--> Retrieval Planner Agent
   |       |
   |       +--> LangSmith span: retrieval_planner_agent
   |
   +--> Separate Vector Store Retrieval
   |       |
   |       +--> LangSmith span: separate_vector_store_retrieval
   |
   +--> Grounded Answer Agent
   |       |
   |       +--> LangSmith span: grounded_answer_agent
   |
   +--> RAG Quality Evaluation
   |       |
   |       +--> LangSmith span: rag_quality_evaluation
   |
   v
Final Answer + Citations + Observability Summary
```

## Folder Structure

```text
20-Module 11-Observability-and-Monitoring-for-Agentic-AI/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── HR/
│   │   └── employee_travel_policy.pdf
│   ├── Sales/
│   │   └── quarterly_sales_pipeline.csv
│   └── Marketing/
│       └── ongoing_campaigns.md
├── lab_agents/
│   ├── __init__.py
│   └── rag_agent.py
├── models/
│   ├── __init__.py
│   └── rag_models.py
└── services/
    ├── __init__.py
    ├── chunking_service.py
    ├── document_loader_service.py
    ├── embedding_service.py
    ├── observability_service.py
    ├── pdf_service.py
    ├── rag_pipeline.py
    └── vector_store_service.py
```

## Tree-Based Call Architecture

```text
main.py
└── run_agentic_rag(question)
    ├── configure_langsmith()
    │   └── config/settings.py
    ├── create_openai_client()
    │   └── config/settings.py
    ├── build_index(openai_client)
    │   ├── load_enterprise_documents()
    │   │   └── services/document_loader_service.py
    │   ├── index_chunks()
    │   │   └── services/vector_store_service.py
    │   └── has_existing_index()
    │       └── services/vector_store_service.py
    ├── select_data_domain()
    │   └── lab_agents/rag_agent.py
    ├── create_retrieval_plan()
    │   └── lab_agents/rag_agent.py
    ├── traced_vector_retrieval()
    │   ├── semantic_search()
    │   └── services/vector_store_service.py
    ├── generate_grounded_answer()
    │   └── lab_agents/rag_agent.py
    ├── evaluate_rag_response()
    │   └── services/observability_service.py
    ├── summarize_retrieved_chunks()
    │   └── services/observability_service.py
    ├── estimate_tokens()
    │   └── services/observability_service.py
    └── format_observability_report()
        └── services/observability_service.py
```

## What Was Added To Lab 13A

This lab is based on the separate-vector-store Agentic RAG pattern from Lab 13A. The following observability features were added:

| Added Feature | File | Purpose |
|---|---|---|
| LangSmith configuration | `config/settings.py` | Loads `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and tracing settings from this lab's `.env`. |
| Top-level workflow trace | `services/rag_pipeline.py` | Traces the full Agentic RAG workflow as one parent run. |
| Agent step traces | `lab_agents/rag_agent.py` | Traces domain routing, retrieval planning, and answer generation. |
| Retrieval trace | `services/rag_pipeline.py` | Traces selected vector store, `top_k`, and retrieved evidence summary. |
| Latency monitoring | `services/observability_service.py` | Measures each workflow step with `time.perf_counter()`. |
| Estimated token usage | `services/observability_service.py` | Estimates tokens for question, retrieval plan, retrieved context, and answer. |
| RAG quality evaluation | `services/observability_service.py` | Scores groundedness, citation usage, relevance, and overall answer quality. |
| Observability summary | `services/rag_pipeline.py` | Prints metrics in the terminal so learners can compare with LangSmith. |

## File Responsibilities

### main.py

Runs the lab in a question loop. The user can ask multiple questions and type `quit` or `exit` to stop.

### config/settings.py

Loads this lab folder's `.env` file, creates Azure OpenAI clients, defines vector-store paths, and configures LangSmith tracing for project `lab20_abhishek`.

### lab_agents/rag_agent.py

Contains the OpenAI Agents SDK agents:

- `select_data_domain()` routes the question to HR, Sales, Marketing, or All.
- `create_retrieval_plan()` explains what the workflow should retrieve.
- `generate_grounded_answer()` creates the final answer from retrieved context.

Each function is decorated with `@traceable` so it appears as a LangSmith span.

### services/rag_pipeline.py

Orchestrates the full Agentic RAG workflow and creates the top-level LangSmith trace. It also collects latency metrics, estimated token counts, retrieval summaries, and evaluation results.

### services/observability_service.py

Contains helper functions for:

- Step latency measurement
- Estimated token usage
- Retrieved chunk summaries
- RAG quality evaluation
- Terminal observability report formatting

### services/vector_store_service.py

Manages separate ChromaDB vector stores for HR, Sales, and Marketing. It searches one selected vector store or all vector stores depending on the domain selected by the agent.

### services/document_loader_service.py

Loads enterprise data from HR PDF, Sales CSV, and Marketing markdown files.

### services/embedding_service.py

Creates embeddings using the Azure OpenAI embedding model.

### models/rag_models.py

Defines dataclasses for source chunks and retrieved chunks.

## LangSmith Project

This lab uses:

```text
LANGSMITH_PROJECT=lab20_abhishek
```

After running the lab, open LangSmith and inspect the project named `lab20_abhishek`.

## Test Prompts And What To Observe In LangSmith

| Objective | Prompt | What To Observe In LangSmith |
|---|---|---|
| Trace AI agent workflow execution | `Which sales region has the highest pipeline risk, and what action should the business take next?` | A parent trace named `lab20_agentic_rag_observability_workflow` with child spans for domain routing, retrieval planning, vector retrieval, answer generation, and RAG evaluation. |
| Monitor latency | `What is the employee travel reimbursement rule for hotel stays?` | Compare span durations in LangSmith with the terminal `Latency by step` section. Domain should usually route to HR. |
| Monitor token usage | `Summarize the active marketing campaigns and recommend which audience should be prioritized.` | Check the terminal `Estimated token usage` section. In LangSmith, inspect inputs/outputs for the plan, retrieved context, and final answer spans. |
| Evaluate RAG quality | `Which sales region has the highest pipeline risk, and what action should the business take next?` | Inspect the `rag_quality_evaluation` span. Look for `overall_score`, `groundedness_score`, `citation_score`, `relevance_score`, and `passed`. |
| Validate vector-store routing | `Compare travel policy considerations with campaign planning risks.` | The domain router may choose `All`. In LangSmith, inspect retrieval inputs and outputs to verify whether multiple business domains were considered. |

## How To Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Expected Learning Outcome

Learners should understand that observability is not only logging the final answer. A production RAG system should expose the full path from user question to agent routing, retrieval, generation, evaluation, and performance metrics.
