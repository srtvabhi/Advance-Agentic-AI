# Lab 19-A Reference

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Environment File

Create `.env` inside this lab folder:

```env
AZURE_OPENAI_ENDPOINT=https://kyndrl77777777.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2025-08-07
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
Embedding_Model=text-embedding-3-large
```

The code loads only this lab's `.env` file:

```python
load_dotenv(BASE_DIR / ".env", override=True)
```

## LangGraph State Syntax

The workflow state is a `TypedDict`.

```python
class ProcurementState(TypedDict):
    request_id: str
    requester_role: Role
    vendor_name: str
    proposal_text: str
    final_status: NotRequired[str]
```

Example:

```python
request = {
    "request_id": "REQ-LOW-001",
    "requester_role": "procurement_analyst",
    "vendor_name": "Northwind Office Supplies",
    "proposal_text": "Annual office-supply agreement.",
}
```

## Node Syntax

A LangGraph node is a normal Python function that receives state and returns updates.

```python
def privacy_guardrail(state: ProcurementState) -> dict[str, Any]:
    redacted, pii_types = redact_pii(state["proposal_text"])
    return {
        "redacted_proposal": redacted,
        "pii_types": pii_types,
    }
```

## Conditional Routing Syntax

Conditional routing decides the next node based on current state.

```python
def route_after_rbac(state: ProcurementState) -> str:
    return "retrieve_policies" if state.get("rbac_allowed") else "finalize_access_denied"
```

Graph example:

```python
graph.add_conditional_edges("rbac_guardrail", route_after_rbac)
```

## Graph Creation Syntax

```python
graph = StateGraph(ProcurementState)
graph.add_node("validate_request", validate_request)
graph.add_edge(START, "validate_request")
graph.add_edge("finalize_recommendation", END)
workflow = graph.compile(checkpointer=InMemorySaver())
```

## Human Approval Syntax

The graph pauses with `interrupt()`.

```python
human_response = interrupt(approval_payload)
```

The graph resumes with `Command(resume=...)`.

```python
result = workflow.invoke(
    Command(resume={
        "decision": "approve",
        "approver_id": "manager-001",
        "approver_role": "procurement_manager",
        "comment": "Approved with controls.",
    }),
    config=config,
)
```

## Retry Syntax

Model-dependent or infrastructure-dependent nodes can use retry policy.

```python
infrastructure_retry = RetryPolicy(max_attempts=3)

graph.add_node(
    "generate_grounded_assessment",
    generate_grounded_assessment,
    retry_policy=infrastructure_retry,
)
```

## Code Explanation

`main.py` accepts one natural-language procurement prompt, infers structured values, and sends one procurement request into the graph.

`build_request_from_prompt()` converts learner text into the `ProcurementState` fields used by LangGraph.

`extract_amount()` finds the purchase amount from text such as `USD 55,000`.

`infer_requester_role()` reads role words such as `employee`, `procurement analyst`, `procurement manager`, or `compliance officer`.

`infer_requested_action()` treats approval language as `approve_purchase`; otherwise it defaults to `review_vendor_risk`.

`infer_data_classification()` reads `public`, `internal`, or `confidential` from the prompt.

`extract_vendor_name()` reads simple patterns such as `Vendor name is Contoso Analytics Services`.

`settings.py` prevents accidental global environment usage by loading `.env` from this lab folder.

`ProcurementState` is the shared memory object for the workflow. Every node adds fields to this state.

`validate_request()` checks required fields such as vendor name, proposal text, and positive purchase amount.

`privacy_guardrail()` redacts email, phone, payment card, and national ID patterns.

`prompt_injection_guardrail()` blocks instructions such as bypass approval, reveal prompt, or ignore system instructions.

`content_filter_guardrail()` blocks severe content such as credential requests and malware language.

`rbac_guardrail()` checks whether the requester role can perform the requested action.

`retrieve_policies()` retrieves approved policy documents using embeddings.

`generate_grounded_assessment()` asks the model to produce a JSON risk assessment based only on approved policy sources.

`output_guardrail()` checks that the model used known source IDs and returned the expected JSON fields.

`determine_approval_requirement()` decides whether procurement manager or compliance officer approval is required. Purchases of USD 25,000 or more require procurement manager approval. Purchases of USD 100,000 or more, or critical-risk requests, require compliance officer approval.

`human_approval_checkpoint()` pauses the workflow and validates the approver role when the graph resumes.

Finalization nodes produce terminal outcomes such as `RECOMMENDATION_READY`, `APPROVED_RECOMMENDATION`, `REJECTED_BY_POLICY`, `ACCESS_DENIED`, or `SECURITY_REVIEW_REQUIRED`.

## Useful Test Scenarios

1. Low-value office-supply request with completed sanctions screening and vendor verification should return `RECOMMENDATION_READY`.
2. High-value confidential-data request should pause for human approval, then finalize based on the grounded policy assessment.
3. Prompt injection text should route to `SECURITY_REVIEW_REQUIRED`.
4. Employee approval request should route to `ACCESS_DENIED`.
5. Proposal with contact details should redact PII before model assessment.
