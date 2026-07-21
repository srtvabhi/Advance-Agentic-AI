# 16-SemanticKernel-Plugins-RAG-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build AI plugins using Semantic Kernel with a RAG-backed HR policy plugin.
User Question
   |
   v

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
semantic-kernel==1.44.0
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
- `from openai import AsyncOpenAI, OpenAI`
- `from semantic_kernel import Kernel`
- `from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_chat_model()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_embedding_model()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_kernel()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


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


def get_chat_model() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_embedding_model() -> str:
    load_environment()
    return os.environ.get("Embedding_Model") or os.environ.get("EMBEDDING_MODEL") or "text-embedding-3-large"


def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"), api_key=get_required_setting("AZURE_OPENAI_API_KEY"))


def create_kernel() -> Kernel:
    load_environment()
    kernel = Kernel()
    async_client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
    kernel.add_service(
        OpenAIChatCompletion(
            ai_model_id=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
            async_client=async_client,
            service_id="foundry-chat",
        )
    )
    return kernel

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from services.plugin_workflow import run_plugin_lab`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from services.plugin_workflow import run_plugin_lab


DEFAULT_QUESTION = "Can I work from home three days a week, and when do I need manager approval?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 16: Build AI Plugins Using Semantic Kernel\n")
    print("Enter a question, press Enter for the default question, or type 'quit' to exit.")

    while True:
        question = input(f"\nDefault question:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()

        if question.casefold() == "quit":
            print("Exiting Lab 16.")
            break

        question = question or DEFAULT_QUESTION
        print("\n" + await run_plugin_lab(question))


if __name__ == "__main__":
    asyncio.run(main())

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

### `plugins/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `plugins/hr_policy_plugin.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from semantic_kernel.functions import kernel_function`
- `from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client`
- `from services.chunking_service import chunk_text`
- `from services.pdf_service import ensure_pdf_exists, read_pdf_pages`
- `from services.vector_store_service import has_existing_index, index_chunks, semantic_search`

Classes:

- `HRPolicyPlugin`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from semantic_kernel.functions import kernel_function

from config.settings import PDF_DIR, SOURCE_DOCS_DIR, create_openai_client
from services.chunking_service import chunk_text
from services.pdf_service import ensure_pdf_exists, read_pdf_pages
from services.vector_store_service import has_existing_index, index_chunks, semantic_search


class HRPolicyPlugin:
    """Semantic Kernel native plugin for HR policy retrieval."""

    def __init__(self) -> None:
        self.openai_client = create_openai_client()
        self.source_file = SOURCE_DOCS_DIR / "hybrid_work_policy.txt"
        self.pdf_file = PDF_DIR / "hybrid_work_policy.pdf"
        self._ensure_index()

    def _ensure_index(self) -> None:
        if has_existing_index():
            print("Using existing ChromaDB vector store. Skipping index build.")
            return

        ensure_pdf_exists(self.source_file, self.pdf_file)
        chunks = []
        for page, text in read_pdf_pages(self.pdf_file):
            chunks.extend(chunk_text(text, self.pdf_file.name, page, "hr-policy"))
        index_chunks(self.openai_client, chunks)

    @kernel_function(name="search_policy", description="Search the HR policy PDF for relevant policy context.")
    def search_policy(self, question: str) -> str:
        results = semantic_search(self.openai_client, question, top_k=3)
        return "\n\n".join(f"Source: {item.citation()}\nContent: {item.text}" for item in results)

    @kernel_function(name="create_hr_ticket", description="Create a simulated HR support ticket.")
    def create_hr_ticket(self, employee_name: str, request_summary: str) -> str:
        return f"Created HR ticket HR-2048 for {employee_name}: {request_summary}"

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

### `services/pdf_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from pathlib import Path`
- `from textwrap import wrap`
- `from pypdf import PdfReader`
- `from reportlab.lib.pagesizes import letter`
- `from reportlab.pdfgen import canvas`

Functions:

- `ensure_pdf_exists()`: Encapsulates reusable logic used by this lab.
- `read_pdf_pages()`: Encapsulates reusable logic used by this lab.

Code:

```python
from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def ensure_pdf_exists(source_path: Path, pdf_path: Path) -> None:
    if pdf_path.exists():
        return

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


def read_pdf_pages(pdf_path: Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(pdf_path))
    return [(index, (page.extract_text() or "").strip()) for index, page in enumerate(reader.pages, start=1)]

```

### `services/plugin_workflow.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from semantic_kernel.functions import KernelArguments`
- `from config.settings import create_kernel`
- `from plugins.hr_policy_plugin import HRPolicyPlugin`

Functions:

- `run_plugin_lab()`: Encapsulates reusable logic used by this lab.

Code:

```python
from semantic_kernel.functions import KernelArguments

from config.settings import create_kernel
from plugins.hr_policy_plugin import HRPolicyPlugin


async def run_plugin_lab(question: str) -> str:
    kernel = create_kernel()
    kernel.add_plugin(HRPolicyPlugin(), plugin_name="HRPolicy")

    context = await kernel.invoke(
        plugin_name="HRPolicy",
        function_name="search_policy",
        question=question,
    )

    answer = await kernel.invoke_prompt(
        (
            "You are an HR policy assistant. Answer the employee question only from the provided policy context. "
            "Mention when an HR ticket is useful.\n\n"
            "Question: {{$question}}\n\nPolicy context:\n{{$context}}\n\nAnswer with citations:"
        ),
        arguments=KernelArguments(question=question, context=str(context)),
    )

    ticket = await kernel.invoke(
        plugin_name="HRPolicy",
        function_name="create_hr_ticket",
        employee_name="Asha",
        request_summary=question,
    )

    return f"--- Retrieved Policy Context ---\n{context}\n\n--- Semantic Kernel Answer ---\n{answer}\n\n--- Native Plugin Action ---\n{ticket}"

```


