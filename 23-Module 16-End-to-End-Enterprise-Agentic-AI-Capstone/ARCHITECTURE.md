# Lab 23: End-to-End Enterprise Agentic AI Capstone

## Objective

Build an end-to-end enterprise Agentic AI solution with a Streamlit user interface.

This capstone demonstrates how an enterprise AI application can combine:

- Multi-domain enterprise knowledge
- Agentic routing
- Retrieval planning
- ChromaDB vector retrieval
- Azure OpenAI answer generation
- LangGraph workflow orchestration
- LangSmith observability
- Streamlit UI deployment readiness

The business problem is enterprise decision support. Business users ask questions across HR, Sales, and Marketing knowledge, and the system selects the correct data domain, retrieves evidence, generates a grounded answer, evaluates RAG quality, and shows observability details.

## Architecture Flow

```text
Business User
   |
   v
Streamlit UI app.py
   |
   v
services/rag_pipeline.py
   |
   v
LangGraph Workflow
   |
   +--> Build or reuse Chroma vector stores
   |
   +--> Domain Router Agent
   |       |
   |       +--> chooses HR, Sales, Marketing, or Enterprise
   |
   +--> Retrieval Planner Agent
   |       |
   |       +--> creates a retrieval strategy
   |
   +--> Retrieval Node
   |       |
   |       +--> HR vector store
   |       +--> Sales vector store
   |       +--> Marketing vector store
   |
   +--> Grounded Answer Agent
   |       |
   |       +--> Azure OpenAI Foundry model
   |
   +--> Token Usage Estimation
   |
   +--> RAG Quality Evaluation
   |
   v
Streamlit Result + LangSmith Trace
```

## Folder Structure

```text
23-Module 16-End-to-End-Enterprise-Agentic-AI-Capstone/
├── .env
├── .env.example
├── app.py
├── main.py
├── requirements.txt
├── ARCHITECTURE.md
├── Reference.md
├── .streamlit/
│   ├── config.toml
│   └── secrets.example.toml
├── config/
│   └── settings.py
├── data/
│   ├── HR/
│   ├── Marketing/
│   └── Sales/
├── graph/
│   └── rag_observability_graph.py
├── lab_agents/
│   └── rag_agent.py
├── models/
│   └── rag_models.py
├── services/
│   ├── document_service.py
│   ├── embedding_service.py
│   ├── observability_service.py
│   ├── rag_pipeline.py
│   ├── retrieval_service.py
│   └── vector_store_service.py
└── vector_store/
    ├── hr_knowledge/
    ├── marketing_knowledge/
    └── sales_knowledge/
```

Note: `vector_store/` is created at runtime. It is not required before the first run.

## Tree-Based Call Architecture

```text
app.py
├── configure_runtime_from_streamlit()
│   ├── config/settings.py -> apply_streamlit_secrets()
│   └── config/settings.py -> configure_langsmith()
├── render_sidebar()
├── run_question()
│   └── services/rag_pipeline.py -> run_agentic_rag()
│       └── graph/rag_observability_graph.py -> build_rag_observability_graph()
│           ├── build_index_node()
│           │   ├── services/document_service.py -> load_enterprise_documents()
│           │   ├── services/document_service.py -> chunk_documents()
│           │   └── services/vector_store_service.py -> index_chunks()
│           ├── domain_router_node()
│           │   └── lab_agents/rag_agent.py -> select_data_domain()
│           ├── retrieval_planner_node()
│           │   └── lab_agents/rag_agent.py -> create_retrieval_plan()
│           ├── retrieval_node()
│           │   └── services/retrieval_service.py -> retrieve_from_selected_domain()
│           ├── answer_node()
│           │   └── lab_agents/rag_agent.py -> generate_grounded_answer()
│           ├── token_usage_node()
│           │   └── services/observability_service.py -> estimate_rag_token_usage()
│           ├── evaluation_node()
│           │   └── services/observability_service.py -> evaluate_rag_response()
│           └── final_output_node()
│               └── services/observability_service.py -> format_observability_report()
└── Streamlit session_state
    └── stores previous questions and answers for the active UI session
```

## File Responsibilities

### app.py

Streamlit UI entry point. It renders the business-question form, sample prompts, sidebar runtime details, workflow output, and session history.

### main.py

Optional terminal entry point. It runs the same capstone workflow without the Streamlit UI.

### config/settings.py

Loads local `.env` values for local development. It also accepts Streamlit Cloud secrets through `apply_streamlit_secrets()`.

### graph/rag_observability_graph.py

Defines the LangGraph workflow. Each node represents one production workflow step.

### lab_agents/rag_agent.py

Contains the LLM-powered agent functions:

- Domain router agent
- Retrieval planner agent
- Grounded answer agent

### services/document_service.py

Loads enterprise documents from the `data/` folders and converts them into chunks.

### services/vector_store_service.py

Builds and reuses ChromaDB vector stores for HR, Sales, and Marketing.

### services/retrieval_service.py

Retrieves relevant chunks from the selected vector store.

### services/observability_service.py

Calculates latency, estimated token usage, retrieved evidence summary, and simple RAG quality scores.

### services/rag_pipeline.py

Single function entry point used by both `app.py` and `main.py`.

### data/

Contains dummy enterprise knowledge for the capstone.

### .streamlit/

Contains Streamlit UI configuration and a sample secrets file for Streamlit Community Cloud.

## Test Prompts

| Objective | Prompt | What To Observe |
|---|---|---|
| Multi-domain routing | Which sales region has the highest pipeline risk, and what action should the business take next? | The workflow should select Sales and cite sales pipeline data. |
| HR decision support | What HR policy should guide an employee relocation request? | The workflow should select HR and answer using HR policy evidence. |
| Marketing analysis | Which marketing campaign needs executive attention and why? | The workflow should select Marketing and retrieve campaign evidence. |
| Enterprise synthesis | Compare sales pipeline risk with current marketing campaign risk. | The workflow may use Enterprise or cross-domain reasoning. |
| Executive-ready output | Create an executive summary using the most relevant enterprise knowledge. | The answer should include grounded recommendations and citations. |

## How To Run Locally

```powershell
cd "23-Module 16-End-to-End-Enterprise-Agentic-AI-Capstone"
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Optional terminal mode:

```powershell
python main.py
```

## Streamlit Community Cloud Deployment

Streamlit Community Cloud is the recommended deployment target for this lab.

1. Push this lab folder to a GitHub repository.
2. Go to:

```text
https://streamlit.io/cloud
```

3. Sign in with GitHub.
4. Choose the repository and branch.
5. Set the main file path:

```text
app.py
```

6. Add secrets in Streamlit app settings:

```toml
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/openai/v1"
AZURE_OPENAI_API_KEY = "your_azure_openai_api_key"
AZURE_OPENAI_API_VERSION = "2025-08-07"
AZURE_OPENAI_DEPLOYMENT = "gpt-5-mini"
Embedding_Model = "text-embedding-3-large"
LANGSMITH_TRACING = "true"
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
LANGSMITH_API_KEY = "your_langsmith_api_key"
LANGSMITH_PROJECT = "lab23_capstone"
```

Do not commit `.env` or real secrets to GitHub.

## Why Not Vercel For This Streamlit Version

Vercel is excellent for frontend apps and serverless functions, but Streamlit expects a running Python web process. For this lab, Streamlit Community Cloud is simpler and better aligned.

If Vercel is required later, the better architecture is:

```text
Next.js frontend on Vercel
Python API backend elsewhere
```

## Key Learning Points

- End-to-end Agentic AI combines UI, orchestration, retrieval, generation, evaluation, and observability.
- LangGraph makes the workflow steps explicit.
- ChromaDB provides local vector search.
- Azure OpenAI generates the routed, grounded answer.
- LangSmith traces the workflow execution.
- Streamlit turns the capstone into an interactive business application.
