# 15-OpenAI-Hybrid-Search-RAG-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Create a hybrid search-based retrieval pipeline using OpenAI, Azure AI Foundry, ChromaDB, semantic search, keyword search, and metadata filtering.
This lab answers support questions from a dummy product support PDF.
User Question
   |

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
chromadb==1.5.9
pypdf==6.14.2
reportlab==5.0.0
```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `agents/__init__.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Code:

```python


```

### `agents/hybrid_rag_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from config.settings import get_chat_model`

Functions:

- `detect_product_filter()`: Encapsulates reusable logic used by this lab.
- `answer_with_hybrid_context()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import get_chat_model


def detect_product_filter(question: str) -> str | None:
    lowered = question.lower()
    if "analyticspro" in lowered or "analytics pro" in lowered:
        return "AnalyticsPro"
    if "securepay" in lowered or "secure pay" in lowered:
        return "SecurePay"
    return None


def answer_with_hybrid_context(client, question: str, results) -> str:
    context = "\n\n".join(
        f"Search type: {item.search_type}\nScore: {item.score:.3f}\nSource: {item.citation()}\nContent: {item.text}"
        for item in results
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support RAG assistant. Use the hybrid search context only. "
                    "Explain the answer simply and include citations."
                ),
            },
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nHybrid search context:\n{context}\n\nAnswer:",
            },
        ],
    )
    return response.choices[0].message.content or ""

```

### `config/__init__.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Code:

```python


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import OpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_embedding_model()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_chat_model()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SOURCE_DOCS_DIR = DATA_DIR / "source_docs"
PDF_DIR = DATA_DIR / "pdfs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def get_embedding_model() -> str:
    load_environment()
    return (
        os.environ.get("Embedding_Model")
        or os.environ.get("EMBEDDING_MODEL")
        or "text-embedding-3-large"
    )


def get_chat_model() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from services.rag_pipeline import run_hybrid_rag`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from services.rag_pipeline import run_hybrid_rag


DEFAULT_QUESTION = (
    "For AnalyticsPro, what should support do when dashboard refresh fails "
    "with token expired and cache mismatch errors?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 15: OpenAI Hybrid Search RAG Pipeline\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    print("\n" + run_hybrid_rag(question))


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/rag_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `DocumentChunk`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.
- `SearchResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    source: str
    page: int
    category: str
    product: str


@dataclass
class SearchResult:
    text: str
    source: str
    page: int
    category: str
    product: str
    score: float
    search_type: str

    def citation(self) -> str:
        return f"{self.source}, page {self.page}, product {self.product}, category {self.category}"

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/chunking_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from models.rag_models import DocumentChunk`

Functions:

- `chunk_text()`: Encapsulates reusable logic used by this lab.

Code:

```python
from models.rag_models import DocumentChunk


def chunk_text(text: str, source: str, page: int, category: str, product: str) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1
    chunk_size = 550
    overlap = 90

    while start < len(words):
        end = start + chunk_size
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-{product}-p{page}-c{chunk_number}",
                text=" ".join(words[start:end]),
                source=source,
                page=page,
                category=category,
                product=product,
            )
        )
        if end >= len(words):
            break
        start = end - overlap
        chunk_number += 1

    return chunks

```

### `services/embedding_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import get_embedding_model`

Functions:

- `create_embedding()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from config.settings import get_embedding_model


def create_embedding(client, text: str) -> list[float]:
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
    return response.data[0].embedding

```

### `services/keyword_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `import re`
- `from models.rag_models import DocumentChunk, SearchResult`

Functions:

- `tokenize()`: Encapsulates reusable logic used by this lab.
- `keyword_search()`: Encapsulates reusable logic used by this lab.

Code:

```python
import re

from models.rag_models import DocumentChunk, SearchResult


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def keyword_search(query: str, chunks: list[DocumentChunk], product_filter: str | None = None) -> list[SearchResult]:
    query_terms = tokenize(query)
    results = []

    for chunk in chunks:
        if product_filter and chunk.product.lower() != product_filter.lower():
            continue

        chunk_terms = tokenize(chunk.text)
        overlap = query_terms.intersection(chunk_terms)
        if not overlap:
            continue

        score = len(overlap) / max(len(query_terms), 1)
        results.append(
            SearchResult(
                text=chunk.text,
                source=chunk.source,
                page=chunk.page,
                category=chunk.category,
                product=chunk.product,
                score=score,
                search_type="keyword",
            )
        )

    return sorted(results, key=lambda item: item.score, reverse=True)

```

### `services/pdf_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from pathlib import Path`
- `from textwrap import wrap`
- `from pypdf import PdfReader`
- `from reportlab.lib.pagesizes import letter`
- `from reportlab.pdfgen import canvas`

Functions:

- `create_pdf_from_text()`: Factory/helper function that creates and returns a configured object used by the lab.
- `ensure_pdf_exists()`: Encapsulates reusable logic used by this lab.
- `read_pdf_pages()`: Encapsulates reusable logic used by this lab.

Code:

```python
from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf_from_text(source_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    text = source_path.read_text(encoding="utf-8")

    pdf = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setFont("Helvetica", 10)

    for paragraph in text.splitlines():
        for line in wrap(paragraph, width=95) or [""]:
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
            pdf.drawString(50, y, line)
            y -= 14
        y -= 6

    pdf.save()


def ensure_pdf_exists(source_path: Path, pdf_path: Path) -> None:
    if not pdf_path.exists():
        create_pdf_from_text(source_path, pdf_path)


def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(pdf_path))
    return [
        (index, (page.extract_text() or "").strip())
        for index, page in enumerate(reader.pages, start=1)
    ]

```

### `services/rag_pipeline.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from agents.hybrid_rag_agent import answer_with_hybrid_context, detect_product_filter`
- `from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client`
- `from services.chunking_service import chunk_text`
- `from services.keyword_service import keyword_search`
- `from services.pdf_service import ensure_pdf_exists, read_pdf_pages`
- `from services.vector_store_service import index_chunks, semantic_search`

Functions:

- `product_section()`: Encapsulates reusable logic used by this lab.
- `load_chunks()`: Encapsulates reusable logic used by this lab.
- `build_index()`: Builds the workflow, graph, pipeline, or reusable application component.
- `deduplicate_results()`: Encapsulates reusable logic used by this lab.
- `run_hybrid_rag()`: Encapsulates reusable logic used by this lab.

Code:

```python
from agents.hybrid_rag_agent import answer_with_hybrid_context, detect_product_filter
from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.keyword_service import keyword_search
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search


SOURCE_FILE = SOURCE_DOCS_DIR / "product_support_kb.txt"
PDF_FILE = PDF_DIR / "product_support_kb.pdf"


def product_section(text: str, product: str) -> str:
    if product == "AnalyticsPro":
        start_marker = "AnalyticsPro overview:"
        end_marker = "SecurePay overview:"
    else:
        start_marker = "SecurePay overview:"
        end_marker = ""

    start = text.find(start_marker)
    if start == -1:
        return text

    end = text.find(end_marker, start + len(start_marker)) if end_marker else -1
    if end == -1:
        return text[start:]
    return text[start:end]


def load_chunks() -> list:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(
            chunk_text(
                product_section(text, "AnalyticsPro"),
                PDF_FILE.name,
                page,
                "support-kb",
                "AnalyticsPro",
            )
        )
        chunks.extend(
            chunk_text(
                product_section(text, "SecurePay"),
                PDF_FILE.name,
                page,
                "support-kb",
                "SecurePay",
            )
        )
    return chunks


def build_index(client, chunks) -> None:
    index_chunks(client, chunks)


def deduplicate_results(results) -> list:
    seen = set()
    unique = []
    for item in sorted(results, key=lambda result: result.score, reverse=True):
        key = (item.search_type, item.source, item.page, item.product, item.text[:80])
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:5]


def run_hybrid_rag(question: str) -> str:
    client = create_openai_client()
    chunks = load_chunks()
    build_index(client, chunks)

    product_filter = detect_product_filter(question)
    semantic_results = semantic_search(client, question, product_filter=product_filter, top_k=4)
    keyword_results = keyword_search(question, chunks, product_filter=product_filter)
    final_results = deduplicate_results(semantic_results + keyword_results)
    answer = answer_with_hybrid_context(client, question, final_results)

    filter_text = product_filter or "No product metadata filter"
    result_map = "\n".join(
        f"- {item.search_type} score={item.score:.3f}: {item.citation()}"
        for item in final_results
    )
    return (
        f"--- Metadata Filter ---\n{filter_text}\n\n"
        f"--- Hybrid Search Results ---\n{result_map}\n\n"
        f"--- Answer ---\n{answer}"
    )

```


