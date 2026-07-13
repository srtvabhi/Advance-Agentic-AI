# 14-OpenAI-Query-Decomposition-RAG-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Implement query decomposition for retrieval using OpenAI, Azure AI Foundry, ChromaDB, and a dummy security runbook PDF.
This lab shows how a complex question can be split into smaller retrieval questions before synthesis.
Complex User Question
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

### `agents/decomposition_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from config.settings import get_chat_model`

Functions:

- `decompose_question()`: Encapsulates reusable logic used by this lab.
- `synthesize_answer()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import get_chat_model


def decompose_question(client, question: str) -> list[str]:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "Break the user question into 3 focused retrieval sub-questions. "
                    "Return only the sub-questions, one per line, without numbering."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    content = response.choices[0].message.content or ""
    return [line.strip(" -1234567890.") for line in content.splitlines() if line.strip()]


def synthesize_answer(client, question: str, sub_questions: list[str], retrieved_chunks) -> str:
    context = "\n\n".join(
        f"Sub-question: {chunk.sub_question}\nSource: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a RAG synthesis agent. Combine evidence from multiple "
                    "retrieval sub-questions. Cite the PDF sources."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original question:\n{question}\n\nSub-questions:\n{sub_questions}\n\n"
                    f"Retrieved evidence:\n{context}\n\nFinal answer:"
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
- `from services.rag_pipeline import run_decomposition_rag`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from services.rag_pipeline import run_decomposition_rag


DEFAULT_QUESTION = (
    "A suspicious login was followed by data export from a finance system. "
    "What should the response team do first, how should severity be assigned, "
    "and what evidence must be preserved?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("Lab 14: OpenAI Query Decomposition RAG\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    print("\n" + run_decomposition_rag(question))


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
    sub_question: str

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


def chunk_text(text: str, source: str, page: int, category: str) -> list[DocumentChunk]:
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1
    chunk_size = 600
    overlap = 100

    while start < len(words):
        end = start + chunk_size
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}-p{page}-c{chunk_number}",
                text=" ".join(words[start:end]),
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

- `from agents.decomposition_agent import decompose_question, synthesize_answer`
- `from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client`
- `from services.chunking_service import chunk_text`
- `from services.pdf_service import ensure_pdf_exists, read_pdf_pages`
- `from services.vector_store_service import index_chunks, search_for_sub_question`

Functions:

- `build_index()`: Builds the workflow, graph, pipeline, or reusable application component.
- `run_decomposition_rag()`: Encapsulates reusable logic used by this lab.

Code:

```python
from agents.decomposition_agent import decompose_question, synthesize_answer
from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import index_chunks, search_for_sub_question


SOURCE_FILE = SOURCE_DOCS_DIR / "security_incident_runbook.txt"
PDF_FILE = PDF_DIR / "security_incident_runbook.pdf"


def build_index(client) -> None:
    ensure_pdf_exists(SOURCE_FILE, PDF_FILE)
    chunks = []
    for page, text in read_pdf_pages(PDF_FILE):
        chunks.extend(chunk_text(text, PDF_FILE.name, page, "incident-response"))
    index_chunks(client, chunks)


def run_decomposition_rag(question: str) -> str:
    client = create_openai_client()
    build_index(client)

    sub_questions = decompose_question(client, question)
    retrieved = []
    for sub_question in sub_questions:
        retrieved.extend(search_for_sub_question(client, sub_question, top_k=2))

    answer = synthesize_answer(client, question, sub_questions, retrieved)
    sub_question_text = "\n".join(f"- {item}" for item in sub_questions)
    citations = "\n".join(f"- {chunk.sub_question}: {chunk.citation()}" for chunk in retrieved)

    return (
        f"--- Decomposed Questions ---\n{sub_question_text}\n\n"
        f"--- Final Answer ---\n{answer}\n\n"
        f"--- Retrieval Map ---\n{citations}"
    )

```


