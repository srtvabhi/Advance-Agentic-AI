# 13-OpenAI-Agentic-RAG-Lab Reference

This reference explains the updated Lab 13 code. The lab now uses three enterprise data folders: HR, Sales, and Marketing.

## Setup

Install dependencies:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
chromadb==1.5.9
pypdf==6.14.2
```

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Data Folders

```text
data/
├── HR/
│   └── employee_travel_policy.pdf
├── Sales/
│   └── quarterly_sales_pipeline.csv
└── Marketing/
    └── ongoing_campaigns.md
```

The question is routed to one of these domains:

```text
HR
Sales
Marketing
All
```

## `main.py`

Purpose: start the lab from the command line.

Important logic:

```python
question = input(...).strip()
result = run_agentic_rag(question)
print(result)
```

It sends the user question to `run_agentic_rag()`.

## `config/settings.py`

Purpose: load this lab's local environment variables and shared paths.

Important paths:

```python
DATA_DIR = BASE_DIR / "data"
HR_DIR = DATA_DIR / "HR"
SALES_DIR = DATA_DIR / "Sales"
MARKETING_DIR = DATA_DIR / "Marketing"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
```

Important functions:

- `load_environment()`: loads only this lab's `.env`.
- `get_embedding_model()`: returns `Embedding_Model` or `EMBEDDING_MODEL`.
- `get_chat_model()`: returns `AZURE_OPENAI_DEPLOYMENT`.
- `create_openai_client()`: creates the OpenAI client for Azure OpenAI.
- `create_agents_run_config()`: connects the OpenAI Agents SDK to the Azure-compatible endpoint and disables OpenAI-platform tracing for this Azure lab.

## `lab_agents/rag_agent.py`

Purpose: contains the real OpenAI Agents SDK reasoning steps. It imports `Agent`, `Runner`, and `RunConfig` from the installed `agents` package.

The local package is named `lab_agents` so it does not shadow the SDK's own `agents` package.

### `select_data_domain(question, run_config)`

Chooses which domain should be searched:

```text
HR, Sales, Marketing, or All
```

Example:

```text
Question about reimbursement -> HR
Question about pipeline risk -> Sales
Question about campaign budget -> Marketing
Question comparing sales and campaigns -> All
```

The router uses the structured `DomainSelection` output model so the result must be `HR`, `Sales`, `Marketing`, or `All`.

### `create_retrieval_plan(question, selected_domain, run_config)`

Creates a short retrieval plan explaining what evidence should be retrieved from the selected domain.

### `generate_grounded_answer(question, selected_domain, plan, retrieved_chunks, run_config)`

Creates the final answer from retrieved context only and includes citations.

## `services/document_loader_service.py`

Purpose: load enterprise data from all department folders.

### `load_hr_documents()`

Reads PDF files from:

```text
data/HR/
```

It calls:

```python
read_pdf_pages()
chunk_text(..., category="HR")
```

### `load_sales_documents()`

Reads CSV files from:

```text
data/Sales/
```

Each CSV row becomes a searchable chunk with:

```python
category="Sales"
```

### `load_marketing_documents()`

Reads Markdown or text files from:

```text
data/Marketing/
```

Campaign notes become searchable chunks with:

```python
category="Marketing"
```

### `load_enterprise_documents()`

Combines all HR, Sales, and Marketing chunks into one list.

## `services/pdf_service.py`

Purpose: read existing PDFs.

### `validate_pdf_exists(pdf_path)`

Raises a clear error if the required PDF is missing.

### `read_pdf_pages(pdf_path)`

Extracts text from every page and returns:

```python
[(page_number, page_text)]
```

## `services/chunking_service.py`

Purpose: split long text into smaller overlapping chunks.

Important settings:

```python
chunk_size=650
overlap=120
```

Overlap helps preserve context between chunks.

## `services/embedding_service.py`

Purpose: convert text into vector embeddings.

Important function:

```python
create_embedding(client, text)
```

This uses the embedding model from `.env`.

## `services/vector_store_service.py`

Purpose: store and search chunks in ChromaDB.

### `index_chunks(openai_client, chunks)`

Stores:

```text
chunk id
text
embedding
source
page
category
```

### `semantic_search(openai_client, query, category_filter, top_k)`

Searches by meaning. If the selected domain is not `All`, it adds a metadata filter:

```python
{"category": "Sales"}
```

That means a Sales question searches Sales chunks first, an HR question searches HR chunks first, and a Marketing question searches Marketing chunks first.

## `services/rag_pipeline.py`

Purpose: orchestrate the full workflow.

Main flow:

```python
client = create_openai_client()
build_index(client)
selected_domain = select_data_domain(client, question)
plan = create_retrieval_plan(client, question, selected_domain)
retrieved_chunks = semantic_search(client, question, category_filter=selected_domain)
answer = generate_grounded_answer(client, question, selected_domain, plan, retrieved_chunks)
```

Output sections:

```text
Selected Data Domain
Retrieval Plan
Answer
Retrieved Citations
```

## `models/rag_models.py`

Purpose: define clean data containers.

### `DocumentChunk`

Stores a chunk before indexing:

```python
chunk_id
text
source
page
category
```

### `RetrievedChunk`

Stores a chunk after retrieval:

```python
text
source
page
category
distance
```

The `citation()` method returns readable source information for the final answer.
