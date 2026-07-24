# Lab 19-A Architecture: Secure Procurement Guardrails Workflow

## Objective

The lab focuses on a procurement team that must review vendor proposals safely before making purchase recommendations. A proposal may contain confidential data, unsafe instructions, unsupported claims, or high-value purchase requests. The workflow must decide whether the request can be finalized, must be blocked, or must pause for human approval.

This lab teaches:

- AI guardrails
- Prompt injection protection
- Privacy redaction
- Content filtering
- Role-based access control
- Retrieval-grounded risk assessment
- Output validation
- Human approval checkpoints
- Auditability and traceability

## Architecture Flow

```text
START
  |
  v
Validate Request
  |
  v
Privacy Guardrail
  |
  v
Prompt Injection Guardrail
  |
  v
Content Filter
  |
  v
RBAC Check
  |
  v
Policy Retrieval
  |
  v
Grounded Risk Assessment
  |
  v
Output Guardrail
  |
  v
Approval Decision
  |
  +--> Human Approval
  |       |
  |       v
  |   Finalization
  |
  +--> Finalization
  |
  v
END
```

Unsafe or unauthorized paths route to controlled terminal states:

```text
Invalid request -> INVALID_REQUEST
Prompt injection -> SECURITY_REVIEW_REQUIRED
Unsafe content -> SECURITY_REVIEW_REQUIRED
RBAC failure -> ACCESS_DENIED
Unsupported output -> SECURITY_REVIEW_REQUIRED
Unauthorized approver -> SECURITY_REVIEW_REQUIRED
Human rejection -> REJECTED_BY_APPROVER
```

## Folder Structure

```text
19-A-Module 10-Secure-Procurement-Guardrails-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── Reference.md
├── config/
│   ├── __init__.py
│   └── settings.py
├── graphs/
│   ├── __init__.py
│   └── procurement_graph.py
├── models/
│   ├── __init__.py
│   └── procurement_models.py
├── nodes/
│   ├── __init__.py
│   └── procurement_nodes.py
└── services/
    ├── __init__.py
    ├── approval_service.py
    ├── audit_service.py
    ├── guardrail_service.py
    ├── llm_service.py
    ├── policy_service.py
    └── rbac_service.py
```

## Tree-Based Call Architecture

```text
main.py
├── load_environment()
│   └── config/settings.py
├── get_sample_requests()
├── build_custom_request()
├── run_request()
│   ├── build_procurement_graph()
│   │   └── graphs/procurement_graph.py
│   │       ├── validate_request()
│   │       ├── privacy_guardrail()
│   │       ├── prompt_injection_guardrail()
│   │       ├── content_filter_guardrail()
│   │       ├── rbac_guardrail()
│   │       ├── retrieve_policies()
│   │       ├── generate_grounded_assessment()
│   │       ├── output_guardrail()
│   │       ├── determine_approval_requirement()
│   │       ├── human_approval_checkpoint()
│   │       └── finalization nodes
│   ├── workflow.invoke(request)
│   ├── Command(resume=approval_response)
│   └── print_result()
│
├── nodes/procurement_nodes.py
│   ├── services/guardrail_service.py
│   │   ├── redact_pii()
│   │   └── detect_patterns()
│   ├── services/rbac_service.py
│   │   └── is_authorized()
│   ├── services/policy_service.py
│   │   ├── ensure_policy_embeddings()
│   │   ├── create_embedding()
│   │   └── retrieve_policy_documents()
│   ├── services/llm_service.py
│   │   └── create_grounded_assessment()
│   ├── services/approval_service.py
│   │   └── get_required_approver()
│   └── services/audit_service.py
│       └── audit_event()
│
└── models/procurement_models.py
    └── ProcurementState
```

## File Responsibilities

### main.py

This is the entry point. It shows a menu of procurement scenarios, runs the LangGraph workflow, handles human approval resume, and prints the final recommendation and audit trail.

### config/settings.py

Loads this lab folder's `.env` file only. It creates the OpenAI client and reads the chat and embedding deployment names.

### models/procurement_models.py

Defines `ProcurementState`, the shared LangGraph state object passed from node to node.

### graphs/procurement_graph.py

Builds the LangGraph workflow. It connects nodes with normal and conditional edges, adds retry policy to infrastructure-sensitive nodes, and enables interrupt/resume behavior with `InMemorySaver`.

### nodes/procurement_nodes.py

Contains the LangGraph node functions. Each node performs one workflow step such as validation, privacy redaction, prompt injection detection, policy retrieval, grounded assessment, output checking, approval routing, or finalization.

### services/guardrail_service.py

Contains deterministic privacy, prompt injection, and content filtering helpers.

### services/rbac_service.py

Contains role-based access rules and authorization checking.

### services/policy_service.py

Stores approved procurement policy documents, creates embeddings, and retrieves the most relevant policy sources.

### services/llm_service.py

Calls the Azure OpenAI chat model to create a grounded procurement risk assessment using only retrieved policy sources.

### services/approval_service.py

Contains approval threshold logic for procurement manager and compliance officer approval.

### services/audit_service.py

Creates audit events with timestamps, node names, decisions, and hashed requester IDs.

## Test Prompts

Use these prompts to test each lab objective. For menu options `1` to `5`, just enter the option number. For custom tests, choose option `6` and enter each value shown in the prompt.

| Lab Objective | Prompt | Expected Behavior |
|---|---|---|
| AI guardrails | `Menu option: 1` | The request passes through validation, privacy, injection, content, RBAC, retrieval, output, approval, and audit controls before finalization. |
| Prompt injection protection | `Menu option: 3` | `prompt_injection_guardrail()` detects unsafe instructions and routes to `SECURITY_REVIEW_REQUIRED`. |
| Privacy redaction | `Menu option: 5` | `privacy_guardrail()` detects and redacts email/phone values before model assessment. |
| Content filtering | `Menu option: 6`<br>`Requester ID: analyst-777`<br>`Requester role: procurement_analyst`<br>`Requested action: review_vendor_risk`<br>`Vendor name: Credential Test Vendor`<br>`Vendor proposal text: To validate this purchase, send us your API key and authentication code.`<br>`Purchase amount USD: 8000`<br>`Data classification: internal` | `content_filter_guardrail()` detects credential-related content and routes to `SECURITY_REVIEW_REQUIRED`. |
| Role-based access control | `Menu option: 4` | `rbac_guardrail()` denies the request because an `employee` cannot perform `approve_purchase`. Final status should be `ACCESS_DENIED`. |
| Retrieval-grounded risk assessment | `Menu option: 1` | `retrieve_policies()` retrieves approved procurement policy sources and `generate_grounded_assessment()` creates a source-grounded risk assessment. |
| Output validation | `Menu option: 1` | `output_guardrail()` verifies required JSON fields and checks that source IDs come from retrieved policies. |
| Human approval checkpoints | `Menu option: 2`<br>`Decision: approve`<br>`Approver role: procurement_manager`<br>`Approver ID: manager-9001`<br>`Approval comment: Approved for lab testing.` | The workflow pauses at `human_approval_checkpoint()` and resumes after authorized approval. Final status should be `APPROVED_RECOMMENDATION`. |
| Auditability and traceability | `Menu option: 1` | The final output includes an audit trail showing each node name and decision. |

## How To Run

From the repository root:

```bash
cd "19-A-Module 10-Secure-Procurement-Guardrails-Lab"
..\.venv\Scripts\python.exe main.py
```

## Expected Learning Outcome

Learners should be able to explain why secure agent workflows need multiple controls before and after model execution. The model is not trusted to enforce every rule by itself. Deterministic checks, RBAC, retrieval grounding, output validation, approval thresholds, and audit logs work together.
