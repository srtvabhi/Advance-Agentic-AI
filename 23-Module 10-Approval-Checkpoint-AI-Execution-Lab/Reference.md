# 23-Module 10-Approval-Checkpoint-AI-Execution-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Add approval checkpoints to AI execution using LangGraph.
This lab shows how an enterprise agent can pause risky actions and create a human approval ticket before execution.
User Role + Requested Action
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
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_openai_client()`: Factory/helper function that creates and returns a configured object used by the lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `get_embedding_model()`: Retrieves information and returns it in a simple format for the agent or workflow.

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
    # Returns the configured chat model deployment.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_embedding_model() -> str:
    # Returns the configured embedding model name.
    load_environment()
    return os.environ.get("Embedding_Model") or "text-embedding-3-large"

```

### `graphs/__init__.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Code:

```python


```

### `graphs/approval_graph.py`

Role: Workflow layer. It defines graph nodes, routing, or orchestration logic.

Key imports:

- `from langgraph.graph import END, StateGraph`
- `from models.approval_models import ApprovalState`
- `from nodes.approval_nodes import audit_node, approval_checkpoint_node, execution_node, final_node, risk_assessment_node, route_after_risk`

Functions:

- `build_approval_graph()`: Builds the workflow, graph, pipeline, or reusable application component.

Code:

```python
from langgraph.graph import END, StateGraph

from models.approval_models import ApprovalState
from nodes.approval_nodes import audit_node, approval_checkpoint_node, execution_node, final_node, risk_assessment_node, route_after_risk


def build_approval_graph():
    # Builds a LangGraph workflow with a human approval checkpoint.
    graph = StateGraph(ApprovalState)
    graph.add_node("risk_assessment", risk_assessment_node)
    graph.add_node("approval_checkpoint", approval_checkpoint_node)
    graph.add_node("execution", execution_node)
    graph.add_node("audit", audit_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("risk_assessment")
    graph.add_conditional_edges(
        "risk_assessment",
        route_after_risk,
        {
            "approval": "approval_checkpoint",
            "execute": "execution",
        },
    )
    graph.add_edge("approval_checkpoint", "audit")
    graph.add_edge("execution", "audit")
    graph.add_edge("audit", "final")
    graph.add_edge("final", END)
    return graph.compile()

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import sys`
- `from graphs.approval_graph import build_approval_graph`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import sys

from graphs.approval_graph import build_approval_graph


DEFAULT_ROLE = "support_agent"
DEFAULT_ACTION = "Delete old customer data from the production database after migration."

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the approval checkpoint lab.
    print("Lab 23: Approval Checkpoints In AI Execution\n")
    role = input(f"Enter user role, or press Enter for default ({DEFAULT_ROLE}): ").strip() or DEFAULT_ROLE
    action = input(f"Enter requested action, or press Enter for default:\n{DEFAULT_ACTION}\n\nAction: ").strip() or DEFAULT_ACTION

    app = build_approval_graph()
    result = app.invoke(
        {
            "user_role": role,
            "requested_action": action,
            "risk_level": "",
            "approval_required": False,
            "approval_reason": "",
            "approval_ticket": "",
            "execution_result": "",
            "audit_record": "",
            "final_output": "",
        }
    )

    print("\n--- Risk Level ---\n", result["risk_level"])
    print("\n--- Approval Required ---\n", result["approval_required"])
    print("\n--- Approval Reason ---\n", result["approval_reason"])
    print("\n--- Approval Ticket ---\n", result["approval_ticket"])
    print("\n--- Execution Result ---\n", result["execution_result"])
    print("\n--- Audit Record ---\n", result["audit_record"])
    print("\n--- Final Explanation ---\n", result["final_output"])


if __name__ == "__main__":
    main()

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/approval_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from typing import TypedDict`

Classes:

- `ApprovalState`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from typing import TypedDict


class ApprovalState(TypedDict):
    # Shared workflow state for approval-based AI execution.
    user_role: str
    requested_action: str
    risk_level: str
    approval_required: bool
    approval_reason: str
    approval_ticket: str
    execution_result: str
    audit_record: str
    final_output: str

```

### `nodes/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `nodes/approval_nodes.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from models.approval_models import ApprovalState`
- `from services.approval_service import create_approval_ticket, evaluate_approval, execute_action`
- `from services.llm_service import ask_model`

Functions:

- `risk_assessment_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `route_after_risk()`: Chooses the next workflow branch or target agent based on the current state/input.
- `approval_checkpoint_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `execution_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `audit_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.
- `final_node()`: Represents one workflow/graph node. It receives state, updates it, and returns the updated state.

Code:

```python
from models.approval_models import ApprovalState
from services.approval_service import create_approval_ticket, evaluate_approval, execute_action
from services.llm_service import ask_model


def risk_assessment_node(state: ApprovalState) -> ApprovalState:
    # Checks role and action risk before execution.
    risk_level, approval_required, reason = evaluate_approval(
        state["user_role"],
        state["requested_action"],
    )
    state["risk_level"] = risk_level
    state["approval_required"] = approval_required
    state["approval_reason"] = reason
    return state


def route_after_risk(state: ApprovalState) -> str:
    # Sends high-risk actions to approval and low-risk actions to execution.
    if state["approval_required"]:
        return "approval"
    return "execute"


def approval_checkpoint_node(state: ApprovalState) -> ApprovalState:
    # Stops execution and creates a human approval ticket.
    state["approval_ticket"] = create_approval_ticket(
        state["user_role"],
        state["requested_action"],
        state["approval_reason"],
    )
    state["execution_result"] = "Execution paused until human approval is completed."
    return state


def execution_node(state: ApprovalState) -> ApprovalState:
    # Executes only when approval is not required.
    state["execution_result"] = execute_action(state["requested_action"])
    return state


def audit_node(state: ApprovalState) -> ApprovalState:
    # Creates an audit trail for governance and compliance review.
    state["audit_record"] = (
        f"Role: {state['user_role']}\n"
        f"Action: {state['requested_action']}\n"
        f"Risk: {state['risk_level']}\n"
        f"Approval required: {state['approval_required']}\n"
        f"Reason: {state['approval_reason']}"
    )
    return state


def final_node(state: ApprovalState) -> ApprovalState:
    # Explains the approval checkpoint result for participants.
    state["final_output"] = ask_model(
        "You are an AI governance trainer.",
        (
            "Explain this human approval checkpoint workflow in simple terms. "
            "Mention why the action was paused or executed.\n\n"
            f"Audit record:\n{state['audit_record']}\n\n"
            f"Approval ticket:\n{state['approval_ticket']}\n\n"
            f"Execution result:\n{state['execution_result']}"
        ),
    )
    return state

```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/approval_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `evaluate_approval()`: Encapsulates reusable logic used by this lab.
- `create_approval_ticket()`: Factory/helper function that creates and returns a configured object used by the lab.
- `execute_action()`: Encapsulates reusable logic used by this lab.

Code:

```python
HIGH_RISK_TERMS = [
    "delete",
    "production",
    "payment",
    "customer data",
    "pii",
    "admin access",
    "refund",
    "database",
]

APPROVER_ROLES = {"security_admin", "compliance_manager", "platform_owner"}


def evaluate_approval(user_role: str, requested_action: str) -> tuple[str, bool, str]:
    # Decides whether an action requires a human approval checkpoint.
    lowered = requested_action.lower()
    is_high_risk = any(term in lowered for term in HIGH_RISK_TERMS)
    role_can_approve = user_role.lower() in APPROVER_ROLES

    if is_high_risk and not role_can_approve:
        return "high", True, "High-risk action requested by a role that cannot self-approve."

    if is_high_risk and role_can_approve:
        return "high", False, "High-risk action requested by an authorized approver role."

    return "low", False, "Low-risk action does not require human approval."


def create_approval_ticket(user_role: str, requested_action: str, reason: str) -> str:
    # Creates a simple simulated approval ticket.
    return (
        "APPROVAL-1001\n"
        f"Requested by: {user_role}\n"
        f"Action: {requested_action}\n"
        f"Reason: {reason}\n"
        "Status: Pending human approval"
    )


def execute_action(requested_action: str) -> str:
    # Simulates execution after approval checks are complete.
    return f"Action executed safely in simulation mode: {requested_action}"

```

### `services/llm_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `from config.settings import create_openai_client, get_model_name`

Functions:

- `ask_model()`: Encapsulates reusable logic used by this lab.

Code:

```python
from config.settings import create_openai_client, get_model_name


def ask_model(system_prompt: str, user_prompt: str) -> str:
    # Sends one chat completion request to the configured Azure AI Foundry model.
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


