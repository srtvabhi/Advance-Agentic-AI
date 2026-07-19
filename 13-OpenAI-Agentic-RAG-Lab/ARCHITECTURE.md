# OpenAI Multi-Domain Enterprise RAG Lab Architecture

## Objective

Build a multi-step Agentic RAG workflow using OpenAI, Azure AI Foundry models, ChromaDB, and multiple enterprise data sources.

This lab demonstrates a more realistic retrieval pattern:

1. Understand the business question.
2. Decide which enterprise data domain is relevant.
3. Retrieve from HR, Sales, Marketing, or all sources.
4. Generate a grounded answer with citations.

## Problem Statement

An enterprise has information spread across departments:

- HR keeps employee policy documents.
- Sales keeps regional pipeline data in CSV format.
- Marketing keeps active campaign notes.

The workflow must decide which data source to use for each question and answer only from retrieved context.

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
   v
Load Enterprise Documents
   |
   +--> data/HR/*.pdf
   |
   +--> data/Sales/*.csv
   |
   +--> data/Marketing/*.md
   |
   v
Chunk Documents
   |
   v
Create Embeddings
   |
   v
Store In ChromaDB
   |
   v
Select Data Domain
   |
   +--> HR
   |
   +--> Sales
   |
   +--> Marketing
   |
   +--> All
   |
   v
Create Retrieval Plan
   |
   v
Filtered Semantic Search
   |
   v
Generate Grounded Answer
   |
   v
Answer With Citations
```

## Folder Structure

```text
13-OpenAI-Agentic-RAG-Lab/
├── .env
├── .env.example
├── ARCHITECTURE.md
├── main.py
├── Reference.md
├── requirements.txt
├── agents/
│   ├── __init__.py
│   └── rag_agent.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── HR/
│   │   └── employee_travel_policy.pdf
│   ├── Marketing/
│   │   └── ongoing_campaigns.md
│   └── Sales/
│       └── quarterly_sales_pipeline.csv
├── models/
│   ├── __init__.py
│   └── rag_models.py
├── services/
│   ├── __init__.py
│   ├── chunking_service.py
│   ├── document_loader_service.py
│   ├── embedding_service.py
│   ├── pdf_service.py
│   ├── rag_pipeline.py
│   └── vector_store_service.py
└── vector_store/
    └── ChromaDB persistent index files
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: run_agentic_rag()
|   from services/rag_pipeline.py
|
|-- function: main()
|   |
|   |-- reads user question
|   |-- calls: run_agentic_rag(question)
|   |-- prints selected domain, retrieval plan, answer, and citations
|
|-- services/rag_pipeline.py
    |
    |-- imports: create_openai_client()
    |   from config/settings.py
    |
    |-- imports: load_enterprise_documents()
    |   from services/document_loader_service.py
    |
    |-- imports: index_chunks(), semantic_search()
    |   from services/vector_store_service.py
    |
    |-- imports agent functions:
    |   |
    |   |-- select_data_domain()
    |   |-- create_retrieval_plan()
    |   |-- generate_grounded_answer()
    |
    |-- function: build_index(openai_client)
    |   |
    |   |-- load_enterprise_documents()
    |   |-- index_chunks(openai_client, chunks)
    |
    |-- function: run_agentic_rag(question)
        |
        |-- create_openai_client()
        |-- build_index(client)
        |-- select_data_domain(client, question)
        |-- create_retrieval_plan(client, question, selected_domain)
        |-- semantic_search(client, question, category_filter=selected_domain)
        |-- generate_grounded_answer(client, question, selected_domain, plan, retrieved_chunks)
        |-- returns final formatted response
```

Document loading chain:

```text
services/document_loader_service.py
|
|-- load_enterprise_documents()
    |
    |-- load_hr_documents()
    |   |
    |   |-- reads data/HR/*.pdf
    |   |-- calls read_pdf_pages()
    |   |-- calls chunk_text(..., category="HR")
    |
    |-- load_sales_documents()
    |   |
    |   |-- reads data/Sales/*.csv
    |   |-- converts each CSV row into business text
    |   |-- creates DocumentChunk(..., category="Sales")
    |
    |-- load_marketing_documents()
        |
        |-- reads data/Marketing/*.md or *.txt
        |-- calls chunk_text(..., category="Marketing")
```

Retrieval chain:

```text
services/vector_store_service.py
|
|-- index_chunks()
|   |
|   |-- create_embedding()
|   |-- stores text, embedding, source, page, and category in ChromaDB
|
|-- semantic_search()
    |
    |-- create_embedding(query)
    |-- applies category filter when selected domain is HR, Sales, or Marketing
    |-- returns RetrievedChunk objects
```

## File Responsibilities

- `.env`: Stores Azure OpenAI endpoint, key, deployment, and embedding model for this lab.
- `.env.example`: Shows required environment variable names without real secrets.
- `main.py`: Command-line entry point that accepts a business question and prints the RAG result.
- `config/settings.py`: Loads this lab's local `.env` file and creates the OpenAI client.
- `agents/rag_agent.py`: Selects the best data domain, creates a retrieval plan, and generates the grounded answer.
- `services/document_loader_service.py`: Loads HR PDFs, Sales CSV rows, and Marketing campaign notes.
- `services/pdf_service.py`: Validates and reads existing PDF files.
- `services/chunking_service.py`: Splits long text into overlapping chunks.
- `services/embedding_service.py`: Creates embeddings using the configured embedding model.
- `services/vector_store_service.py`: Stores and searches chunks in ChromaDB with optional domain filtering.
- `services/rag_pipeline.py`: Orchestrates the full multi-domain RAG workflow.
- `models/rag_models.py`: Defines `DocumentChunk` and `RetrievedChunk` dataclasses.
- `data/HR/employee_travel_policy.pdf`: HR policy PDF used for employee travel, approval, and reimbursement questions.
- `data/Sales/quarterly_sales_pipeline.csv`: Sales pipeline data by region and product.
- `data/Marketing/ongoing_campaigns.md`: Marketing campaign notes, goals, status, and recommended actions.
- `vector_store/`: Stores the persistent ChromaDB index.

## Test Prompts

Use these prompts to test the lab objective:

1. Which sales region has the highest pipeline risk, and what action should the business take next?
2. Can an employee book a business class flight for a 9 hour international trip, and what approval or receipt rules apply?
3. Which active campaign should receive more webinar retargeting budget?
4. Compare renewal risk between AnalyticsPro sales pipeline and the current AnalyticsPro renewal campaign.
5. What should leadership do this quarter to improve SecurePay revenue and campaign conversion?

## How To Run

```bash
cd "13-OpenAI-Agentic-RAG-Lab"
..\.venv\Scripts\python.exe main.py
```
