# 13-OpenAI-Agentic-RAG-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build a multi-step Agentic RAG workflow using OpenAI, Azure AI Foundry models, ChromaDB, and a dummy PDF document.
This lab answers questions from an existing enterprise travel policy PDF.
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

### `agents/rag_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from config.settings import get_chat_model`

Functions:

- `create_retrieval_plan()`: Factory/helper function that creates and returns a configured object used by the lab.
- `generate_grounded_answer()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import get_chat_model


def create_retrieval_plan(client, question: str) -> str:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a retrieval planner. Create a short plan for answering "
                    "the question from enterprise policy documents. Use 3 bullets."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""


def generate_grounded_answer(client, question: str, plan: str, retrieved_chunks) -> str:
    context = "\n\n".join(
        f"Source: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise RAG assistant. Answer only from the provided context. "
                    "If context is missing, say what is missing. Pay close attention to "
                    "threshold words such as over, under, between, before, and after. "
                    "Include short citations."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\nRetrieval plan:\n{plan}\n\n"
                    f"Retrieved context:\n{context}\n\nAnswer:"
                ),
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
- `from services.rag_pipeline import run_agentic_rag`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from services.rag_pipeline import run_agentic_rag


DEFAULT_QUESTION = (
    "Can an employee book a business class flight for a 9 hour international trip, "
    "and what approval or receipt rules apply?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 13: OpenAI Multi-Step Agentic RAG Workflow\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    result = run_agentic_rag(question)
    print("\n" + result)


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
- `RetrievedChunk`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

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


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int
    category: str
    distance: float

    def citation(self) -> str:
        return f"{self.source}, page {self.page}, category {self.category}"

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


def chunk_text(
    text: str,
    source: str,
    page: int,
    category: str,
    chunk_size: int = 650,
    overlap: int = 120,
) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_value = " ".join(chunk_words)
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-p{page}-c{chunk_number}",
                text=chunk_text_value,
                source=source,
                page=page,
                category=category,
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

### `services/pdf_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from pathlib import Path`
- `from pypdf import PdfReader`

Functions:

- `validate_pdf_exists()`: Confirms the required PDF is available before indexing starts.
- `read_pdf_pages()`: Encapsulates reusable logic used by this lab.

Code:

```python
from pathlib import Path

from pypdf import PdfReader


def validate_pdf_exists(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Required PDF not found: {pdf_path}. "
            "Place employee_travel_policy.pdf inside data/pdfs before running the lab."
        )


def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    validate_pdf_exists(pdf_path)
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    return pages

```

### `services/rag_pipeline.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import PDF_DIR, create_openai_client`
- `from services.chunking_service import chunk_text`
- `from services.pdf_service import read_pdf_pages`
- `from services.vector_store_service import index_chunks, semantic_search`
- `from agents.rag_agent import create_retrieval_plan, generate_grounded_answer`

Functions:

- `build_index()`: Builds the workflow, graph, pipeline, or reusable application component.
- `run_agentic_rag()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import PDF_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import read_pdf_pages
from services.vector_store_service import index_chunks, semantic_search
from agents.rag_agent import create_retrieval_plan, generate_grounded_answer


PDF_FILE = PDF_DIR / "employee_travel_policy.pdf"


def build_index(openai_client) -> None:
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(
            chunk_text(
                text=text,
                source=PDF_FILE.name,
                page=page,
                category="travel-policy",
            )
        )
    index_chunks(openai_client, chunks)


def run_agentic_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    plan = create_retrieval_plan(client, question)
    retrieved_chunks = semantic_search(client, question, top_k=4)
    answer = generate_grounded_answer(client, question, plan, retrieved_chunks)

    citations = "\n".join(f"- {chunk.citation()}" for chunk in retrieved_chunks)
    return (
        f"--- Retrieval Plan ---\n{plan}\n\n"
        f"--- Answer ---\n{answer}\n\n"
        f"--- Retrieved Citations ---\n{citations}"
    )

```


