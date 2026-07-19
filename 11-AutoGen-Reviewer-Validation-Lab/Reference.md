# 11-AutoGen-Reviewer-Validation-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Implement a reviewer-validation agent pattern using AutoGen.
Create and validate an enterprise policy for AI agents that can access customer data and send external emails.
The workflow creates a first draft, asks a reviewer to validate it, and performs one revision cycle when the reviewer returns `REVISION_REQUIRED`.

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2
autogen-agentchat==0.7.5
autogen-ext==0.7.5

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

### `agents/reviewer_agents.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from autogen_agentchat.agents import AssistantAgent`

Functions:

- `create_policy_writer()`: Factory/helper function that creates and returns a configured object used by the lab.
- `create_validation_reviewer()`: Factory/helper function that creates and returns a configured object used by the lab.

Code explanation:

- `create_policy_writer()` creates the drafting agent and tells it which policy sections must be included.
- `create_validation_reviewer()` creates the reviewer agent and gives it a validation checklist.
- The reviewer must end with either `APPROVED` or `REVISION_REQUIRED`, so the workflow can make a clear decision.

Code:

```python
from autogen_agentchat.agents import AssistantAgent


def create_policy_writer(model_client):
    return AssistantAgent(
        name="policy_writer",
        model_client=model_client,
        system_message=(
            "You are a policy writer. Draft a practical enterprise policy. "
            "Include purpose, scope, access control, controls, human approval workflow, "
            "logging, risk handling, policy owner, audit evidence, and exception handling. "
            "Keep the draft concise and learner friendly."
        ),
    )


def create_validation_reviewer(model_client):
    return AssistantAgent(
        name="validation_reviewer",
        model_client=model_client,
        system_message=(
            "You are a validation reviewer. Review the policy against this checklist: "
            "purpose, scope, access control, human approval, logging, risk handling, owner, and audit evidence. "
            "Keep the review concise. End with either APPROVED or REVISION_REQUIRED."
        ),
    )

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
- `from autogen_ext.models.openai import OpenAIChatCompletionClient`
- `from dotenv import load_dotenv`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `create_model_client()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
import os
from pathlib import Path

from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_model_client() -> OpenAIChatCompletionClient:
    load_environment()
    return OpenAIChatCompletionClient(
        model=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )


```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `import sys`
- `from config.settings import create_model_client`
- `from orchestration.review_workflow import run_review_workflow`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio
import sys

from config.settings import create_model_client
from orchestration.review_workflow import run_review_workflow


DEFAULT_TASK = (
    "Create a one-page enterprise policy for AI agents that can access customer data "
    "and send external emails."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 11: AutoGen Reviewer Validation Pattern\n")
    task = input(f"Enter policy task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    try:
        result = await run_review_workflow(model_client, task)
        print("\n--- Validation Result ---\n")
        print(result.to_text())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())

```

### `models/__init__.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Code:

```python


```

### `models/validation_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `ValidationResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code explanation:

- `draft` stores the first policy created by the writer.
- `review` stores the first reviewer feedback.
- `status` stores the final validation result.
- `revised_draft` and `final_review` are populated only when the first review asks for revision.
- `to_text()` formats the complete result for the terminal.

Code:

```python
from dataclasses import dataclass


@dataclass
class ValidationResult:
    draft: str
    review: str
    status: str
    revised_draft: str = ""
    final_review: str = ""
    revision_performed: bool = False

    def to_text(self) -> str:
        output = (
            f"Validation Status: {self.status}\n\n"
            f"--- Draft ---\n{self.draft}\n\n"
            f"--- Review ---\n{self.review}"
        )

        if self.revision_performed:
            output += (
                f"\n\n--- Revised Draft ---\n{self.revised_draft}\n\n"
                f"--- Final Review ---\n{self.final_review}"
            )

        return output


```

### `orchestration/__init__.py`

Role: Supporting Python file used by this lab.

Code:

```python


```

### `orchestration/review_workflow.py`

Role: Supporting Python file used by this lab.

Key imports:

- `from agents.reviewer_agents import create_policy_writer, create_validation_reviewer`
- `from models.validation_models import ValidationResult`
- `from services.validation_service import validate_review`

Functions:

- `run_review_workflow()`: Encapsulates reusable logic used by this lab.

Code explanation:

- The writer creates the first draft.
- The reviewer checks the draft against the checklist.
- `validate_review()` reads the reviewer decision.
- If the first draft is approved, the workflow returns immediately.
- If revision is required, reviewer feedback is sent back to the writer.
- The reviewer checks the revised draft again, and that becomes the final validation status.

Code:

```python
from agents.reviewer_agents import create_policy_writer, create_validation_reviewer
from models.validation_models import ValidationResult
from services.validation_service import validate_review


async def run_review_workflow(model_client, task: str) -> ValidationResult:
    writer = create_policy_writer(model_client)
    reviewer = create_validation_reviewer(model_client)

    draft_result = await writer.run(task=task)
    draft = draft_result.messages[-1].content

    review_task = f"Review this policy draft:\n\n{draft}"
    review_result = await reviewer.run(task=review_task)
    review = review_result.messages[-1].content

    status = validate_review(str(review))
    if status == "APPROVED":
        return ValidationResult(draft=str(draft), review=str(review), status=status)

    revision_task = (
        "Revise the policy draft using the reviewer feedback. "
        "Make sure the revised policy explicitly includes purpose, scope, access control, "
        "human approval, logging, risk handling, policy owner, audit evidence, and exception handling.\n\n"
        f"Original task:\n{task}\n\n"
        f"Original draft:\n{draft}\n\n"
        f"Reviewer feedback:\n{review}"
    )
    revised_result = await writer.run(task=revision_task)
    revised_draft = revised_result.messages[-1].content

    final_review_task = f"Review this revised policy draft:\n\n{revised_draft}"
    final_review_result = await reviewer.run(task=final_review_task)
    final_review = final_review_result.messages[-1].content
    final_status = validate_review(str(final_review))

    return ValidationResult(
        draft=str(draft),
        review=str(review),
        status=final_status,
        revised_draft=str(revised_draft),
        final_review=str(final_review),
        revision_performed=True,
    )


```

### `services/__init__.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Code:

```python


```

### `services/validation_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Functions:

- `validate_review()`: Checks, validates, or reviews workflow output before the final response.

Code explanation:

- The reviewer writes a natural-language review, but the application needs a simple status.
- This function looks for the final decision line.
- If the final decision contains `APPROVED`, the lab prints approved.
- If the final decision contains `REVISION_REQUIRED`, the lab triggers or reports revision required.

Code:

```python
def validate_review(review_text: str) -> str:
    text = review_text.upper()

    # Prefer the reviewer's final decision line instead of any earlier mention.
    decision_lines = [
        line.strip()
        for line in text.splitlines()
        if "APPROVED" in line or "REVISION_REQUIRED" in line
    ]
    final_decision = decision_lines[-1] if decision_lines else text

    if "REVISION_REQUIRED" in final_decision:
        return "REVISION_REQUIRED"
    if "APPROVED" in final_decision:
        return "APPROVED"
    return "REVISION_REQUIRED"

```


