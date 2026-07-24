import json

from models.support_models import SupportWorkflowState
from services.knowledge_service import retrieve_knowledge
from services.model_gateway import AllModelTargetsFailed, call_model_with_fallback
from services.policy_service import check_response_policy
from services.security_service import find_pii, redact_pii


# Add a small trace event to the workflow state.
def append_trace(state: SupportWorkflowState, node: str, status: str, **details) -> list[dict]:
    trace = list(state.get("trace", []))
    trace.append({"node": node, "status": status, **details})
    return trace


# Validate that the incoming support ticket has enough information to process.
def validate_ticket(state: SupportWorkflowState) -> dict:
    if not state.get("subject", "").strip() or not state.get("body", "").strip():
        error = "Ticket subject and body are required."
        return {
            "validation_error": error,
            "route": "failed",
            "errors": [*state.get("errors", []), error],
            "trace": append_trace(state, "validate_ticket", "failed", error=error),
        }

    return {
        "validation_error": "",
        "route": "continue",
        "trace": append_trace(state, "validate_ticket", "completed"),
    }


# Detect and redact PII before ticket text is sent to model-backed nodes.
def protect_sensitive_data(state: SupportWorkflowState) -> dict:
    pii_types = find_pii(state["body"])
    return {
        "contains_pii": bool(pii_types),
        "redacted_body": redact_pii(state["body"]),
        "trace": append_trace(state, "protect_sensitive_data", "completed", pii_detected=pii_types),
    }


# Classify ticket intent and urgency using primary/fallback model gateway.
def classify_ticket(state: SupportWorkflowState) -> dict:
    system_prompt = """
Classify an enterprise customer-support ticket.
Return only valid JSON with:
intent: billing | account_access | service_incident | general_support
urgency: low | medium | high | critical
confidence: number from 0.0 to 1.0
reason: short explanation
"""
    user_prompt = json.dumps(
        {
            "subject": state["subject"],
            "body": state["redacted_body"],
            "channel": state["channel"],
        }
    )

    try:
        output, metadata = call_model_with_fallback(system_prompt, user_prompt)
        parsed = json.loads(output)
        intent = parsed.get("intent", "general_support")
        urgency = parsed.get("urgency", "medium")
        confidence = float(parsed.get("confidence", 0.0))
        return {
            "intent": intent if intent in {"billing", "account_access", "service_incident", "general_support"} else "general_support",
            "urgency": urgency if urgency in {"low", "medium", "high", "critical"} else "medium",
            "confidence": max(0.0, min(1.0, confidence)),
            "classification_reason": parsed.get("reason", ""),
            "model_target": metadata["target"],
            "model_used": metadata["deployment"],
            "retry_count": state.get("retry_count", 0) + metadata["retry_count"],
            "fallback_activated": state.get("fallback_activated", False) or metadata["fallback_activated"],
            "model_failures": [*state.get("model_failures", []), *metadata["previous_failures"]],
            "route": "continue",
            "trace": append_trace(state, "classify_ticket", "completed", target=metadata["target"]),
        }
    except AllModelTargetsFailed as exc:
        return {
            "route": "human_review",
            "model_failures": [*state.get("model_failures", []), *exc.failures],
            "trace": append_trace(state, "classify_ticket", "model_failed"),
        }
    except (json.JSONDecodeError, ValueError) as exc:
        return {
            "route": "human_review",
            "errors": [*state.get("errors", []), f"Classification output could not be parsed: {exc}"],
            "trace": append_trace(state, "classify_ticket", "parse_failed"),
        }


# Decide whether the ticket can continue automatically or must go to a human.
def assess_risk(state: SupportWorkflowState) -> dict:
    reasons = []
    if state.get("urgency") in {"high", "critical"}:
        reasons.append("high urgency")
    if state.get("confidence", 0.0) < 0.75:
        reasons.append("low classification confidence")
    if state.get("contains_pii", False):
        reasons.append("sensitive data detected")
    if state.get("intent") == "service_incident":
        reasons.append("service incident requires human oversight")

    route = "human_review" if reasons else "continue"
    return {
        "route": route,
        "trace": append_trace(state, "assess_risk", "completed", route=route, reasons=reasons),
    }


# Retrieve approved support knowledge for the classified ticket.
def retrieve_knowledge_node(state: SupportWorkflowState) -> dict:
    documents = retrieve_knowledge(
        state.get("intent", "general_support"),
        state["subject"],
        state["redacted_body"],
    )
    return {
        "retrieved_documents": documents,
        "trace": append_trace(
            state,
            "retrieve_knowledge",
            "completed",
            document_ids=[document["id"] for document in documents],
        ),
    }


# Generate a customer-facing draft using approved knowledge only.
def generate_response(state: SupportWorkflowState) -> dict:
    system_prompt = """
You are an enterprise customer-support assistant.
Create a concise customer-facing draft response.
Rules:
1. Use only the supplied approved knowledge.
2. Never request passwords, authentication codes, payment-card numbers, or secrets.
3. Never guarantee refunds, restoration, or resolution times.
4. Do not claim an action occurred unless the context confirms it.
"""
    user_prompt = json.dumps(
        {
            "ticket": {
                "subject": state["subject"],
                "body": state["redacted_body"],
                "intent": state.get("intent"),
                "urgency": state.get("urgency"),
            },
            "approved_knowledge": state.get("retrieved_documents", []),
        }
    )

    try:
        output, metadata = call_model_with_fallback(system_prompt, user_prompt)
        return {
            "draft_response": output.strip(),
            "model_target": metadata["target"],
            "model_used": metadata["deployment"],
            "retry_count": state.get("retry_count", 0) + metadata["retry_count"],
            "fallback_activated": state.get("fallback_activated", False) or metadata["fallback_activated"],
            "model_failures": [*state.get("model_failures", []), *metadata["previous_failures"]],
            "route": "continue",
            "trace": append_trace(state, "generate_response", "completed", target=metadata["target"]),
        }
    except AllModelTargetsFailed as exc:
        return {
            "route": "human_review",
            "model_failures": [*state.get("model_failures", []), *exc.failures],
            "trace": append_trace(state, "generate_response", "model_failed"),
        }


# Check the response against deterministic safety rules.
def policy_check(state: SupportWorkflowState) -> dict:
    passed, reason = check_response_policy(state.get("draft_response", ""))
    return {
        "policy_passed": passed,
        "policy_reason": reason,
        "route": "auto_response" if passed else "human_review",
        "trace": append_trace(state, "policy_check", "completed", passed=passed),
    }


# Finalize a successful automated response.
def finalize_auto_response(state: SupportWorkflowState) -> dict:
    return {
        "final_status": "AUTO_RESPONSE_READY",
        "final_response": state["draft_response"],
        "trace": append_trace(state, "finalize_auto_response", "completed"),
    }


# Prepare a human-review package when risk, policy, or model reliability requires it.
def prepare_human_review(state: SupportWorkflowState) -> dict:
    summary = (
        "HUMAN_REVIEW_REQUIRED\n\n"
        f"Ticket: {state['ticket_id']}\n"
        f"Subject: {state['subject']}\n"
        f"Intent: {state.get('intent', 'unknown')}\n"
        f"Urgency: {state.get('urgency', 'unknown')}\n"
        f"PII detected: {state.get('contains_pii', False)}\n"
        f"Fallback activated: {state.get('fallback_activated', False)}\n"
        f"Policy reason: {state.get('policy_reason', 'Not checked')}\n"
        f"Draft response: {state.get('draft_response', 'No draft created')}"
    )
    return {
        "final_status": "HUMAN_REVIEW_REQUIRED",
        "final_response": summary,
        "trace": append_trace(state, "prepare_human_review", "completed"),
    }


# Finalize invalid tickets.
def finalize_failure(state: SupportWorkflowState) -> dict:
    return {
        "final_status": "FAILED",
        "final_response": state.get("validation_error", "Ticket failed validation."),
        "trace": append_trace(state, "finalize_failure", "completed"),
    }
