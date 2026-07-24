# Lab 19 Reference

This lab implements a production-style customer-support workflow using LangGraph.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

`.env.example` includes primary and fallback model settings:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_FALLBACK_ENDPOINT=
AZURE_OPENAI_FALLBACK_API_KEY=
AZURE_OPENAI_FALLBACK_DEPLOYMENT=
```

If fallback settings are not provided, the code defaults fallback values to the primary target.

## `main.py`

Purpose: collect a support ticket and run the LangGraph workflow.

Important functions:

```python
build_ticket_from_input()
print_result()
main()
```

Explanation:

- `build_ticket_from_input()` lets learners enter subject, body, and channel.
- `main()` builds the graph and invokes it with the ticket.
- `print_result()` displays final status, response, retry count, fallback status, model failures, and trace.

## `models/support_models.py`

Purpose: define workflow state.

Important model:

```python
class SupportWorkflowState(TypedDict):
```

Explanation:

- The state stores ticket input.
- It also stores PII status, classification, retrieved documents, model telemetry, routing, final response, and trace.
- Every LangGraph node reads and updates this state.

## `graphs/support_workflow_graph.py`

Purpose: define LangGraph nodes and conditional routes.

Important function:

```python
build_support_workflow_graph()
```

Important routes:

```python
route_after_validation()
route_after_classification()
route_after_risk()
route_after_generation()
route_after_policy()
```

Explanation:

- Invalid tickets go to `finalize_failure`.
- Model failure, high risk, PII, low confidence, or policy failure goes to `prepare_human_review`.
- Safe tickets go to `finalize_auto_response`.

## `nodes/support_nodes.py`

Purpose: implement the business workflow steps.

Main nodes:

| Node | Purpose |
|---|---|
| `validate_ticket()` | Checks required subject/body |
| `protect_sensitive_data()` | Detects and redacts PII |
| `classify_ticket()` | Classifies intent and urgency using retry/fallback gateway |
| `assess_risk()` | Routes risky tickets to human review |
| `retrieve_knowledge_node()` | Gets approved support knowledge |
| `generate_response()` | Generates customer response using retry/fallback gateway |
| `policy_check()` | Blocks unsafe generated responses |
| `finalize_auto_response()` | Marks response ready for auto-send |
| `prepare_human_review()` | Creates human-review package |
| `finalize_failure()` | Ends invalid tickets |

## `services/model_gateway.py`

Purpose: implement production-style model reliability.

Important functions:

```python
call_single_target_with_retry()
call_model_with_fallback()
is_retryable_exception()
calculate_backoff()
```

Flow:

```text
Model request
   |
   +-- Try primary deployment up to 3 times
   |
   +-- If primary is exhausted, activate fallback
   |
   +-- Try fallback deployment up to 3 times
   |
   +-- If all targets fail, raise AllModelTargetsFailed
```

Explanation:

- Transient errors are retried.
- Non-retryable errors fail fast and move to fallback.
- Fallback activation is recorded in workflow state.
- If every target fails, the graph routes the ticket to human review.

## `services/security_service.py`

Purpose: protect sensitive customer data.

Important functions:

```python
find_pii()
redact_pii()
```

Explanation:

- Detects email, phone, and payment-card patterns.
- Redacts values before model-backed nodes use ticket text.

## `services/knowledge_service.py`

Purpose: retrieve approved support knowledge.

Important function:

```python
retrieve_knowledge()
```

Explanation:

- Uses a small approved knowledge base.
- Scores documents by intent and keywords.
- Returns top knowledge items for response generation.

## `services/policy_service.py`

Purpose: prevent unsafe automated responses.

Important function:

```python
check_response_policy()
```

Explanation:

- Blocks empty responses.
- Blocks unsafe phrases such as asking for passwords or promising guaranteed refunds.
- Failed policy checks route to human review.

## What Learners Should Notice

This lab demonstrates production patterns through execution:

- Validation before processing
- PII protection before model calls
- Explicit retry and fallback
- Approved knowledge retrieval
- Safety policy checks
- Human-review route
- Trace and reliability telemetry
