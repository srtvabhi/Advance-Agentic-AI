# 27-Module 11-RAG-Quality-Evaluation-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Evaluate RAG response quality using LangGraph, optional LangSmith tracing, and an LLM-as-a-judge evaluation step.
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
langgraph==1.2.9
langchain-core==1.4.9
langsmith==0.10.1
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
- `from openai import OpenAI`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `configure_langsmith()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    # Loads this lab's local .env file.
    load_dotenv(BASE_DIR / ".env", override=True)


def configure_langsmith() -> bool:
    # Enables LangSmith only when students add their own key.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    tracing_requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and tracing_requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required local environment setting.
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> OpenAI:
    # Creates an OpenAI-compatible client for Azure AI Foundry.
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    # Returns the configured Foundry chat deployment.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/rag_eval_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.rag_eval_models import RAGEvaluationState`
- `from nodes.rag_eval_nodes import generate_answer_node, llm_as_judge_node, observability_report_node, retrieve_context_node`

Functions:

- `build_rag_eval_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.rag_eval_models import RAGEvaluationState
from nodes.rag_eval_nodes import generate_answer_node, llm_as_judge_node, observability_report_node, retrieve_context_node


def build_rag_eval_graph():
    # Builds a LangGraph workflow for RAG response evaluation.
    graph = StateGraph(RAGEvaluationState)
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("generate_answer", generate_answer_node)
    graph.add_node("llm_as_judge", llm_as_judge_node)
    graph.add_node("observability_report", observability_report_node)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "generate_answer")
    graph.add_edge("generate_answer", "llm_as_judge")
    graph.add_edge("llm_as_judge", "observability_report")
    graph.add_edge("observability_report", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from config.settings import configure_langsmith`
- `from graphs.rag_eval_graph import build_rag_eval_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from config.settings import configure_langsmith
from graphs.rag_eval_graph import build_rag_eval_graph


DEFAULT_QUESTION = "How quickly should payroll questions be handled, and when should HR requests be escalated?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the RAG quality evaluation lab.
    langsmith_enabled = configure_langsmith()
    print("Lab 27: Evaluate RAG Response Quality With Observability\n")
    print(f"LangSmith tracing enabled: {langsmith_enabled}\n")

    question = input(f"Enter RAG question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    app = build_rag_eval_graph()
    result = app.invoke(
        {
            "question": question,
            "retrieved_context": "",
            "answer": "",
            "evaluation": "",
            "observability_report": "",
        }
    )

    print("\n--- Retrieved Context ---\n", result["retrieved_context"])
    print("\n--- RAG Answer ---\n", result["answer"])
    print("\n--- LLM-As-Judge Evaluation ---\n", result["evaluation"])
    print("\n--- Observability Report ---\n", result["observability_report"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/rag_eval_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `RAGEvaluationState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class RAGEvaluationState(TypedDict):
    # Shared state for RAG answer generation and evaluation.
    question: str
    retrieved_context: str
    answer: str
    evaluation: str
    observability_report: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/rag_eval_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from langsmith import traceable`
- `from models.rag_eval_models import RAGEvaluationState`
- `from services.llm_service import ask_model`
- `from services.retrieval_service import retrieve_context`

Functions:

- `retrieve_context_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `generate_answer_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `llm_as_judge_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `observability_report_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from langsmith import traceable

from models.rag_eval_models import RAGEvaluationState
from services.llm_service import ask_model
from services.retrieval_service import retrieve_context


@traceable(name="retrieve_context_node", run_type="retriever")
def retrieve_context_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Retrieves policy context for the user's question.
    state["retrieved_context"] = retrieve_context(state["question"])
    return state


@traceable(name="generate_answer_node", run_type="chain")
def generate_answer_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Generates a RAG answer grounded in retrieved context.
    state["answer"] = ask_model(
        "You are an HR policy assistant. Answer only from the provided context. If context is insufficient, say what is missing.",
        f"Question: {state['question']}\n\nContext:\n{state['retrieved_context']}",
    )
    return state


@traceable(name="llm_as_judge_node", run_type="chain")
def llm_as_judge_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Evaluates answer quality using an LLM-as-a-judge prompt.
    state["evaluation"] = ask_model(
        "You are a strict RAG evaluator.",
        (
            "Evaluate the answer against the retrieved context. Score each item from 1 to 5: "
            "groundedness, relevance, completeness, and safety. Then give one improvement suggestion.\n\n"
            f"Question: {state['question']}\n\n"
            f"Retrieved context:\n{state['retrieved_context']}\n\n"
            f"Answer:\n{state['answer']}"
        ),
    )
    return state


@traceable(name="observability_report_node", run_type="chain")
def observability_report_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Creates a practical observability report for participants.
    state["observability_report"] = (
        "RAG observability report:\n"
        "1. Retrieval step captured the context used by the answer.\n"
        "2. Generation step captured the final answer.\n"
        "3. Evaluation step scored groundedness, relevance, completeness, and safety.\n"
        "4. In LangSmith, students can inspect each step as a trace when LANGSMITH_TRACING=true."
    )
    return state

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from langsmith import traceable`
- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_model()`: Encapsulates reusable logic used by this lab.

Code:

```python
from langsmith import traceable

from config.settings import create_openai_client, get_model_name


@traceable(name="rag_foundry_chat_completion", run_type="llm")
def ask_model(system_prompt: str, user_prompt: str) -> str:
    # Sends one traced chat completion request to Azure AI Foundry.
    client = create_openai_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

```

### `services/retrieval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from pathlib import Path`

Functions:

- `load_documents()`: Encapsulates reusable logic used by this lab.
- `retrieve_context()`: Encapsulates reusable logic used by this lab.

Code:

```python
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "hr_policy_knowledge_base.txt"


def load_documents() -> list[str]:
    # Loads a tiny local knowledge base for the RAG evaluation lab.
    text = DATA_FILE.read_text(encoding="utf-8")
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def retrieve_context(question: str, top_k: int = 2) -> str:
    # Performs simple keyword retrieval so participants can focus on observability.
    documents = load_documents()
    question_terms = {term.strip(".,?:;").lower() for term in question.split() if len(term) > 3}

    scored = []
    for document in documents:
        document_lower = document.lower()
        score = sum(1 for term in question_terms if term in document_lower)
        scored.append((score, document))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [document for score, document in scored[:top_k] if score > 0]
    if not selected:
        selected = documents[:top_k]
    return "\n\n".join(selected)

```


