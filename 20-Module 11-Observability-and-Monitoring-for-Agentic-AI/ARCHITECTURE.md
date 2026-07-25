# Lab 20 Architecture: Observability and Monitoring for Agentic RAG

## Objective

This lab implements observability for an Agentic RAG workflow using LangGraph, Azure OpenAI, and LangSmith.

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
- Automatic LLM token usage from LangChain model spans
- Estimated token usage for non-LLM sections such as retrieved context
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
   +--> build_rag_observability_graph()
           |
           v
        LangGraph Workflow
           |
           +--> build_or_reuse_vector_indexes
           |       |
           |       +--> HR data --------> vector_store/hr_knowledge
           |       +--> Sales data -----> vector_store/sales_knowledge
           |       +--> Marketing data -> vector_store/marketing_knowledge
   |
           +--> domain_router_agent
           |       |
           |       +--> LangChain ChatOpenAI LLM span with token usage
   |
           +--> retrieval_planner_agent
           |       |
           |       +--> LangChain ChatOpenAI LLM span with token usage
   |
           +--> separate_vector_store_retrieval
   |
           +--> grounded_answer_agent
           |       |
           |       +--> LangChain ChatOpenAI LLM span with token usage
   |
           +--> token_usage_estimation
   |
           +--> rag_quality_evaluation
   |
           +--> format_final_output
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
├── graph/
│   ├── __init__.py
│   └── rag_observability_graph.py
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
    ├── build_rag_observability_graph()
    │   └── graph/rag_observability_graph.py
    │       ├── build_index_node()
    │       │   ├── load_enterprise_documents()
    │       │   ├── index_chunks()
    │       │   └── has_existing_index()
    │       ├── domain_router_node()
    │       │   └── select_data_domain()
    │       │       └── ChatOpenAI.invoke()
    │       ├── retrieval_planner_node()
    │       │   └── create_retrieval_plan()
    │       │       └── ChatOpenAI.invoke()
    │       ├── retrieval_node()
    │       │   └── traced_vector_retrieval()
    │       │       └── semantic_search()
    │       ├── answer_node()
    │       │   └── generate_grounded_answer()
    │       │       └── ChatOpenAI.invoke()
    │       ├── token_usage_node()
    │       │   └── estimate_rag_token_usage()
    │       ├── evaluation_node()
    │       │   └── evaluate_rag_response()
    │       └── final_output_node()
    │           └── format_observability_report()
    └── workflow.invoke()
```

## What Was Added To Lab 13A

This lab is based on the separate-vector-store Agentic RAG pattern from Lab 13A. The following observability features were added:

| Added Feature | File | Purpose |
|---|---|---|
| LangSmith configuration | `config/settings.py` | Loads `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and tracing settings from this lab's `.env`. |
| LangGraph workflow | `graph/rag_observability_graph.py` | Defines graph nodes and edges for the full RAG observability workflow. |
| Top-level workflow trace | `services/rag_pipeline.py` | Traces the full LangGraph Agentic RAG workflow as one parent run. |
| Agent step traces | `lab_agents/rag_agent.py` | Traces domain routing, retrieval planning, and answer generation helper functions. |
| Automatic LLM token usage | `lab_agents/rag_agent.py` and `config/settings.py` | Uses LangChain `ChatOpenAI`, so LangSmith can show token usage on nested LLM spans. |
| Retrieval trace | `graph/rag_observability_graph.py` | Traces selected vector store, `top_k`, and retrieved evidence summary. |
| Latency monitoring | `services/observability_service.py` | Measures each workflow step with `time.perf_counter()`. |
| Estimated token usage | `services/observability_service.py` | Creates a `token_usage_estimation` span for non-LLM text sections. Exact LLM token usage is visible on LangChain `ChatOpenAI` spans. |
| RAG quality evaluation | `services/observability_service.py` | Scores groundedness, citation usage, relevance, and overall answer quality. |
| Observability summary | `services/rag_pipeline.py` | Prints metrics in the terminal so learners can compare with LangSmith. |

## File Responsibilities

### main.py

Runs the lab in a question loop. The user can ask multiple questions and type `quit` or `exit` to stop.

### config/settings.py

Loads this lab folder's `.env` file, creates Azure OpenAI clients, creates the LangChain `ChatOpenAI` model, defines vector-store paths, and configures LangSmith tracing for project `lab20_abhishek`.

### graph/rag_observability_graph.py

Defines the LangGraph workflow. Each node performs one step: build/reuse indexes, route domain, plan retrieval, search vector store, generate answer, estimate tokens, evaluate answer quality, and format final output.

### lab_agents/rag_agent.py

Contains LangChain-powered agent helper functions:

- `select_data_domain()` routes the question to HR, Sales, Marketing, or All.
- `create_retrieval_plan()` explains what the workflow should retrieve.
- `generate_grounded_answer()` creates the final answer from retrieved context.

Each function is decorated with `@traceable`, and each model call uses `ChatOpenAI.invoke()` so LangSmith can show nested LLM spans with token usage.

### services/rag_pipeline.py

Configures LangSmith, builds the LangGraph workflow, invokes it, and returns the final output.

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
| Monitor token usage | `Summarize the active marketing campaigns and recommend which audience should be prioritized.` | Click nested `ChatOpenAI` LLM spans under `domain_router_agent`, `retrieval_planner_agent`, or `grounded_answer_agent` to see provider token usage. Click `token_usage_estimation` for estimated non-LLM text sizes. |
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
