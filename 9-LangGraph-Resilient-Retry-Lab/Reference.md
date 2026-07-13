# 9-LangGraph-Resilient-Retry-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Develop a resilient multi-agent workflow with retries.
Process a vendor invoice, validate required fields, verify the vendor, retry a temporary vendor API failure, and produce a finance approval recommendation.
Invoice Text
   |

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
langgraph==1.2.9
langchain-core==1.4.9
tenacity==9.1.4

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> AsyncOpenAI:
    load_environment()
    return AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


```

### `graph/resilient_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.checkpoint.memory import InMemorySaver`
- `from langgraph.graph import END, START, StateGraph`
- `from models.state_models import ResilientState`
- `from nodes.approval_node import approval_node`
- `from nodes.extract_node import extract_node`
- `from nodes.final_node import final_node`
- `from nodes.validate_node import validate_node`
- `from nodes.vendor_node import vendor_node`

Functions:

- `route_after_validation()`: Chooses the next workflow branch or target agent based on the current state/input.
- `route_after_vendor_check()`: Chooses the next workflow branch or target agent based on the current state/input.
- `build_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from models.state_models import ResilientState
from nodes.approval_node import approval_node
from nodes.extract_node import extract_node
from nodes.final_node import final_node
from nodes.validate_node import validate_node
from nodes.vendor_node import vendor_node


def route_after_validation(state: ResilientState) -> str:
    if state["validation_status"] == "invalid":
        return "final"
    return "vendor"


def route_after_vendor_check(state: ResilientState) -> str:
    if state["vendor_status"] == "success":
        return "approval"
    if state.get("retry_count", 0) < 2:
        return "vendor"
    return "final"


def build_graph():
    graph = StateGraph(ResilientState)

    graph.add_node("extract", extract_node)
    graph.add_node("validate", validate_node)
    graph.add_node("vendor", vendor_node)
    graph.add_node("approval", approval_node)
    graph.add_node("final", final_node)

    graph.add_edge(START, "extract")
    graph.add_edge("extract", "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {"vendor": "vendor", "final": "final"},
    )
    graph.add_conditional_edges(
        "vendor",
        route_after_vendor_check,
        {"vendor": "vendor", "approval": "approval", "final": "final"},
    )
    graph.add_edge("approval", "final")
    graph.add_edge("final", END)

    return graph.compile(checkpointer=InMemorySaver())


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from graph.resilient_graph import build_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from graph.resilient_graph import build_graph


DEFAULT_INVOICE = (
    "Vendor: Contoso Cloud Services. Amount: 15000 USD. "
    "Due date: 2026-08-15. Purpose: Annual cloud monitoring renewal."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 9: LangGraph Resilient Workflow With Retries\n")
    invoice = input(f"Enter invoice text, or press Enter for default:\n{DEFAULT_INVOICE}\n\nInvoice: ").strip()
    invoice = invoice or DEFAULT_INVOICE

    app = build_graph()
    result = await app.ainvoke(
        {"invoice_text": invoice, "retry_count": 0},
        config={"configurable": {"thread_id": "invoice-demo-1"}},
    )

    print("\n--- Final Response ---\n")
    print(result["final_response"])


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/state_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import Literal, TypedDict`

Classes:

- `ResilientState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import Literal, TypedDict


class ResilientState(TypedDict, total=False):
    invoice_text: str
    extracted_data: str
    validation_status: Literal["valid", "invalid"]
    vendor_status: Literal["success", "failed"]
    retry_count: int
    error: str
    approval: str
    final_response: str


```

### `nodes/approval_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import ResilientState`
- `from services.llm_service import ask_llm`

Functions:

- `approval_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import ResilientState
from services.llm_service import ask_llm


async def approval_node(state: ResilientState) -> ResilientState:
    approval = await ask_llm(
        "You are a finance approval assistant.",
        (
            "Review this invoice and recommend approve, reject, or manual review.\n\n"
            f"Extracted data:\n{state['extracted_data']}\n\n"
            f"Vendor status:\n{state['error']}"
        ),
    )
    return {"approval": approval}


```

### `nodes/extract_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import ResilientState`
- `from services.llm_service import ask_llm`

Functions:

- `extract_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import ResilientState
from services.llm_service import ask_llm


async def extract_node(state: ResilientState) -> ResilientState:
    extracted_data = await ask_llm(
        "You extract invoice fields.",
        f"Extract vendor, amount, due date, and risk notes from this invoice:\n{state['invoice_text']}",
    )
    return {"extracted_data": extracted_data}


```

### `nodes/final_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import ResilientState`

Functions:

- `final_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import ResilientState


async def final_node(state: ResilientState) -> ResilientState:
    if state.get("validation_status") == "invalid":
        return {"final_response": f"Workflow stopped: {state['error']}"}

    if state.get("vendor_status") == "failed":
        return {"final_response": f"Workflow failed after retries: {state['error']}"}

    return {
        "final_response": (
            "Resilient workflow completed.\n\n"
            f"Retries used: {state.get('retry_count', 0)}\n\n"
            f"Extracted data:\n{state['extracted_data']}\n\n"
            f"Approval recommendation:\n{state['approval']}"
        )
    }


```

### `nodes/validate_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import ResilientState`

Functions:

- `validate_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import ResilientState


async def validate_node(state: ResilientState) -> ResilientState:
    text = state["invoice_text"].lower()
    is_valid = "amount" in text and "vendor" in text

    if is_valid:
        return {"validation_status": "valid", "error": ""}

    return {
        "validation_status": "invalid",
        "error": "Invoice must include vendor and amount.",
    }


```

### `nodes/vendor_node.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.state_models import ResilientState`
- `from services.vendor_service import TemporaryVendorError, verify_vendor`

Functions:

- `vendor_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.state_models import ResilientState
from services.vendor_service import TemporaryVendorError, verify_vendor


async def vendor_node(state: ResilientState) -> ResilientState:
    retry_count = state.get("retry_count", 0)

    try:
        status = verify_vendor(retry_count)
        return {
            "vendor_status": "success",
            "error": status,
            "retry_count": retry_count,
        }
    except TemporaryVendorError as exc:
        return {
            "vendor_status": "failed",
            "error": str(exc),
            "retry_count": retry_count + 1,
        }


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_llm()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import create_openai_client, get_model_name


async def ask_llm(system_prompt: str, user_prompt: str) -> str:
    client = create_openai_client()
    response = await client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


```

### `services/vendor_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Classes:

- `TemporaryVendorError`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Functions:

- `verify_vendor()`: Encapsulates reusable logic used by this lab.

Code:

```python
class TemporaryVendorError(Exception):
    pass


def verify_vendor(retry_count: int) -> str:
    # Simulate a recoverable external API failure on the first attempt.
    if retry_count == 0:
        raise TemporaryVendorError("Vendor API timeout. Retry required.")

    return "Vendor verified successfully on retry."


```


