# Lab 13A Reference

This reference explains the important code pattern used in Lab 13A.

## Main Difference

Lab 13A uses **different vector stores for different data stores**.

```text
HR data        -> vector_store/hr_knowledge
Sales data     -> vector_store/sales_knowledge
Marketing data -> vector_store/marketing_knowledge
```

This is useful when enterprise teams want stronger separation between departments or data domains.

## `main.py`

`main.py` runs the lab in a question loop.

```python
while True:
    question = input("Question: ").strip()

    if question.lower() in {"quit", "exit"}:
        break

    question = question or DEFAULT_QUESTION
    result = run_agentic_rag(question)
```

Explanation:

- The user can ask multiple questions in one run.
- Pressing Enter uses the default Sales question.
- Typing `quit` or `exit` stops the lab.

## `config/settings.py`

This file defines one vector-store folder per domain.

```python
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
HR_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "hr_knowledge"
SALES_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "sales_knowledge"
MARKETING_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "marketing_knowledge"
```

Explanation:

- HR embeddings are stored separately from Sales and Marketing.
- Sales embeddings are stored separately from HR and Marketing.
- Marketing embeddings are stored separately from HR and Sales.

## `services/document_loader_service.py`

This file loads all enterprise data sources.

Important functions:

```python
load_hr_documents()
load_sales_documents()
load_marketing_documents()
load_enterprise_documents()
```

Explanation:

- `load_hr_documents()` reads HR PDFs.
- `load_sales_documents()` reads Sales CSV rows.
- `load_marketing_documents()` reads Marketing notes.
- `load_enterprise_documents()` combines all chunks for indexing.

Each chunk has a category:

```python
category="HR"
category="Sales"
category="Marketing"
```

That category decides which vector store receives the chunk.

## `services/vector_store_service.py`

This is the most important file in Lab 13A.

### Domain Store Mapping

```python
DOMAIN_STORE_DIRS = {
    "HR": HR_VECTOR_STORE_DIR,
    "Sales": SALES_VECTOR_STORE_DIR,
    "Marketing": MARKETING_VECTOR_STORE_DIR,
}
```

Explanation:

- The dictionary maps a business domain to its vector-store folder.
- The router agent chooses a domain.
- The retrieval service searches the matching vector store.

### Create Domain Client

```python
def get_chroma_client(domain: str):
    store_dir = DOMAIN_STORE_DIRS[domain]
    store_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(store_dir))
```

Explanation:

- If domain is `HR`, ChromaDB uses `vector_store/hr_knowledge`.
- If domain is `Sales`, ChromaDB uses `vector_store/sales_knowledge`.
- If domain is `Marketing`, ChromaDB uses `vector_store/marketing_knowledge`.

### Index Chunks

```python
def index_chunks(openai_client, chunks):
    chunks_by_domain = {
        "HR": [chunk for chunk in chunks if chunk.category == "HR"],
        "Sales": [chunk for chunk in chunks if chunk.category == "Sales"],
        "Marketing": [chunk for chunk in chunks if chunk.category == "Marketing"],
    }
```

Explanation:

- Chunks are grouped by domain.
- Each group is embedded and saved into its own vector store.
- Existing vector stores are reused and skipped.

### Search Selected Store

```python
def semantic_search(openai_client, query, category_filter="All", top_k=4):
    if category_filter in DOMAIN_STORE_DIRS:
        return search_domain(openai_client, query, category_filter, top_k)
```

Explanation:

- If router selects `HR`, only HR vector store is searched.
- If router selects `Sales`, only Sales vector store is searched.
- If router selects `Marketing`, only Marketing vector store is searched.
- If router selects `All`, all vector stores are searched and merged.

## `lab_agents/rag_agent.py`

This file contains the OpenAI Agents SDK reasoning steps.

Important functions:

```python
select_data_domain()
create_retrieval_plan()
generate_grounded_answer()
```

Explanation:

- `select_data_domain()` decides whether the question belongs to HR, Sales, Marketing, or All.
- `create_retrieval_plan()` explains how retrieval should happen.
- `generate_grounded_answer()` answers only from retrieved chunks and includes citations.

## Full Workflow

```text
User asks question
   |
   v
Domain Router Agent chooses HR, Sales, Marketing, or All
   |
   v
Vector store service searches selected store
   |
   v
Retrieval Planner Agent explains the search plan
   |
   v
Grounded Answer Agent creates answer with citations
```

## Best Prompts

```text
Which sales region has the highest pipeline risk, and what action should the business take next?
```

```text
What is the travel reimbursement policy for client visits?
```

```text
Which marketing campaign should be prioritized for enterprise customers?
```

```text
Compare HR travel rules and Marketing campaign actions for a customer event.
```

```text
What should the business do if sales risk is high but marketing campaigns are already active?
```
