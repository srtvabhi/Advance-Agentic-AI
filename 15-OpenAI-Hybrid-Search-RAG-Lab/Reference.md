# 15-OpenAI-Hybrid-Search-RAG-Lab Reference

This reference explains the Lab 15 code. The lab now uses only the existing product support PDF as the retrieval source.

## Lab Summary

Lab 15 builds a hybrid search retrieval pipeline for product support questions.

It combines:

- Semantic search using ChromaDB and embeddings
- Keyword search using exact term overlap
- Product metadata filtering for `AnalyticsPro` and `SecurePay`
- Deduplication before final answer generation

## Environment And Setup

Pinned dependencies from `requirements.txt`:

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

## Data Source

The lab uses this existing PDF:

```text
data/pdfs/product_support_kb.pdf
```

There is no duplicate `.txt` source file and no PDF generation step.

## `main.py`

Purpose: start the lab from the command line.

Main logic:

```python
question = input(...).strip()
print(run_hybrid_rag(question))
```

The default question tests AnalyticsPro metadata filtering and hybrid retrieval.

## `config/settings.py`

Purpose: load local `.env` values and define shared paths.

Important paths:

```python
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
```

Important functions:

- `load_environment()`: loads this lab's `.env`.
- `get_embedding_model()`: returns the embedding model.
- `get_chat_model()`: returns the chat deployment name.
- `create_openai_client()`: creates the Azure OpenAI client.
- `create_agents_run_config()`: connects the OpenAI Agents SDK to the Azure-compatible endpoint and disables OpenAI-platform tracing for this Azure lab.

## `lab_agents/hybrid_rag_agent.py`

Purpose: detect the product filter and run the real OpenAI Agents SDK support-answer agent. It imports `Agent`, `Runner`, and `RunConfig` from the installed `agents` package.

The local package is named `lab_agents` so it does not shadow the SDK's own `agents` package.

### `detect_product_filter(question)`

Checks whether the question mentions:

```text
AnalyticsPro
SecurePay
```

If found, that product is used as metadata filter.

### `answer_with_hybrid_context(question, results, run_config)`

Runs the `Hybrid Search Support Agent` through `Runner.run_sync()` using the merged hybrid search results to create a grounded answer with citations.

## `services/pdf_service.py`

Purpose: validate and read the existing PDF.

### `validate_pdf_exists(pdf_path)`

Checks that the required PDF exists:

```text
data/pdfs/product_support_kb.pdf
```

If missing, it raises a clear `FileNotFoundError`.

### `read_pdf_pages(pdf_path)`

Extracts text from each PDF page and returns:

```python
[(page_number, page_text)]
```

## `services/chunking_service.py`

Purpose: split product support text into product-aware chunks.

Main function:

```python
chunk_text(text, source, page, category, product)
```

Each chunk stores:

```text
source
page
category
product
```

Product metadata is important for filtering AnalyticsPro and SecurePay results.

## `services/embedding_service.py`

Purpose: create embeddings for semantic search.

Main function:

```python
create_embedding(client, text)
```

It sends text to the configured embedding model and returns a vector.

## `services/keyword_service.py`

Purpose: perform exact-term keyword search.

### `tokenize(text)`

Converts text into lowercase searchable terms.

### `keyword_search(query, chunks, product_filter)`

Finds chunks that share words with the question.

This is helpful for exact error messages such as:

```text
token expired
cache mismatch
webhook
settlement
```

## `services/vector_store_service.py`

Purpose: manage ChromaDB semantic search.

### `index_chunks(openai_client, chunks)`

Stores:

```text
chunk id
text
embedding
source
page
category
product
```

### `semantic_search(openai_client, query, product_filter, top_k)`

Searches by meaning and optionally filters by product metadata.

Example:

```python
where={"product": "AnalyticsPro"}
```

## `services/rag_pipeline.py`

Purpose: orchestrate the full hybrid search workflow.

Main flow:

```python
client = create_openai_client()
chunks = load_chunks()
build_index(client, chunks)
product_filter = detect_product_filter(question)
semantic_results = semantic_search(client, question, product_filter=product_filter)
keyword_results = keyword_search(question, chunks, product_filter=product_filter)
final_results = deduplicate_results(semantic_results + keyword_results)
answer = answer_with_hybrid_context(client, question, final_results)
```

Output sections:

```text
Metadata Filter
Hybrid Search Results
Answer
```

## `models/rag_models.py`

Purpose: define structured data containers.

### `DocumentChunk`

Represents a support chunk before indexing.

### `SearchResult`

Represents a retrieved result from semantic or keyword search.

The `citation()` method returns readable source, page, product, and category information.
