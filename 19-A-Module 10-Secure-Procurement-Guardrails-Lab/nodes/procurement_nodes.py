import json
from typing import Any

from langgraph.types import interrupt

from models.procurement_models import ProcurementState
from services.approval_service import get_required_approver
from services.audit_service import audit_event, stable_hash
from services.guardrail_service import (
    CONTENT_PATTERNS,
    INJECTION_PATTERNS,
    detect_patterns,
    redact_pii,
)
from services.llm_service import create_grounded_assessment
from services.policy_service import PROHIBITED_VENDORS, retrieve_policy_documents
from services.rbac_service import is_authorized


# Validate required business fields before any security or model work begins.
def validate_request(state: ProcurementState) -> dict[str, Any]:
    errors: list[str] = []
    if not state.get("vendor_name", "").strip():
        errors.append("Vendor name is required.")
    if not state.get("proposal_text", "").strip():
        errors.append("Proposal text is required.")
    if state.get("purchase_amount_usd", 0) <= 0:
        errors.append("Purchase amount must be positive.")

    route = "blocked" if errors else "continue"
    return {
        "validation_errors": errors,
        "route": route,
        "audit_log": audit_event(state, "validate_request", route, error_count=len(errors)),
    }


# Redact basic PII so sensitive values are not sent to the model.
def privacy_guardrail(state: ProcurementState) -> dict[str, Any]:
    redacted, pii_types = redact_pii(state["proposal_text"])
    return {
        "redacted_proposal": redacted,
        "pii_types": pii_types,
        "audit_log": audit_event(
            state,
            "privacy_guardrail",
            "redacted" if pii_types else "no_pii_detected",
            pii_types=pii_types,
        ),
    }


# Block prompt injection before the proposal reaches the model.
def prompt_injection_guardrail(state: ProcurementState) -> dict[str, Any]:
    signals = detect_patterns(state["redacted_proposal"], INJECTION_PATTERNS)
    detected = bool(signals)
    return {
        "injection_detected": detected,
        "injection_signals": signals,
        "route": "security_review" if detected else "continue",
        "audit_log": audit_event(
            state,
            "prompt_injection_guardrail",
            "blocked" if detected else "passed",
            signals=signals,
        ),
    }


# Detect unsafe content categories such as credential requests or exploit language.
def content_filter_guardrail(state: ProcurementState) -> dict[str, Any]:
    categories = detect_patterns(state["redacted_proposal"], CONTENT_PATTERNS)
    severe = any(category in {"credential_request", "malware_or_exploit"} for category in categories)
    return {
        "content_categories": categories,
        "route": "security_review" if severe else "continue",
        "audit_log": audit_event(
            state,
            "content_filter_guardrail",
            "blocked" if severe else "passed",
            categories=categories,
        ),
    }


# Enforce role-based access control before retrieval and assessment.
def rbac_guardrail(state: ProcurementState) -> dict[str, Any]:
    allowed = is_authorized(state["requester_role"], state["requested_action"])
    return {
        "rbac_allowed": allowed,
        "route": "continue" if allowed else "access_denied",
        "audit_log": audit_event(
            state,
            "rbac_guardrail",
            "allowed" if allowed else "denied",
            requester_role=state["requester_role"],
            requested_action=state["requested_action"],
        ),
    }


# Retrieve only approved enterprise procurement policies for grounding.
def retrieve_policies(state: ProcurementState) -> dict[str, Any]:
    query = (
        f"Vendor: {state['vendor_name']}\n"
        f"Purchase amount: {state['purchase_amount_usd']}\n"
        f"Data classification: {state['data_classification']}\n"
        f"Proposal: {state['redacted_proposal']}"
    )
    try:
        selected = retrieve_policy_documents(query)
    except Exception as exc:
        return {
            "route": "security_review",
            "errors": [*state.get("errors", []), f"Policy retrieval failed: {exc}"],
            "audit_log": audit_event(state, "retrieve_policies", "failed"),
        }

    return {
        "retrieved_policies": selected,
        "route": "continue",
        "audit_log": audit_event(
            state,
            "retrieve_policies",
            "completed",
            source_ids=[item["id"] for item in selected],
        ),
    }


# Generate a risk assessment using the redacted proposal and approved policy sources.
def generate_grounded_assessment(state: ProcurementState) -> dict[str, Any]:
    try:
        assessment = create_grounded_assessment(
            vendor_name=state["vendor_name"],
            purchase_amount_usd=state["purchase_amount_usd"],
            data_classification=state["data_classification"],
            redacted_proposal=state["redacted_proposal"],
            retrieved_policies=state["retrieved_policies"],
        )
    except Exception as exc:
        return {
            "route": "security_review",
            "errors": [*state.get("errors", []), f"Assessment failed: {exc}"],
            "audit_log": audit_event(state, "generate_grounded_assessment", "failed"),
        }

    return {
        "assessment": assessment,
        "audit_log": audit_event(
            state,
            "generate_grounded_assessment",
            "completed",
            recommendation=assessment.get("recommendation"),
            risk_level=assessment.get("risk_level"),
        ),
    }


# Check that the model used known policy sources and returned the required schema.
def output_guardrail(state: ProcurementState) -> dict[str, Any]:
    assessment = state.get("assessment", {})
    approved_source_ids = {item["id"] for item in state.get("retrieved_policies", [])}
    unsupported_claims: list[str] = []

    for claim in assessment.get("claims", []):
        source_id = claim.get("source_id")
        if source_id not in approved_source_ids:
            unsupported_claims.append(claim.get("claim", "Unnamed claim"))

    unknown_sources = set(assessment.get("source_ids", [])) - approved_source_ids
    if unknown_sources:
        unsupported_claims.append("Unknown source IDs: " + ", ".join(sorted(unknown_sources)))

    required_fields = {
        "summary",
        "risk_level",
        "risk_reasons",
        "required_controls",
        "recommendation",
        "source_ids",
        "claims",
    }
    missing_fields = required_fields - set(assessment)
    if missing_fields:
        unsupported_claims.append("Missing fields: " + ", ".join(sorted(missing_fields)))

    if state["vendor_name"] in PROHIBITED_VENDORS and assessment.get("recommendation") != "reject":
        unsupported_claims.append("Prohibited vendor was not rejected.")

    passed = not unsupported_claims
    return {
        "grounded": passed,
        "unsupported_claims": unsupported_claims,
        "output_guardrail_passed": passed,
        "route": "continue" if passed else "security_review",
        "audit_log": audit_event(
            state,
            "output_guardrail",
            "passed" if passed else "blocked",
            unsupported_claims=unsupported_claims,
        ),
    }


# Decide if the recommendation can finalize or must pause for a human approver.
def determine_approval_requirement(state: ProcurementState) -> dict[str, Any]:
    assessment = state.get("assessment", {})
    required_role = get_required_approver(
        amount=state["purchase_amount_usd"],
        risk_level=assessment.get("risk_level", "high"),
        recommendation=assessment.get("recommendation", "reject"),
    )
    approval_required = bool(required_role)
    return {
        "approval_required": approval_required,
        "required_approver_role": required_role,
        "route": "approval" if approval_required else "finalize",
        "audit_log": audit_event(
            state,
            "determine_approval_requirement",
            "approval_required" if approval_required else "no_approval_required",
            required_role=required_role,
        ),
    }


# Pause the graph for human approval and validate the approver role when resumed.
def human_approval_checkpoint(state: ProcurementState) -> dict[str, Any]:
    approval_payload = {
        "request_id": state["request_id"],
        "vendor_name": state["vendor_name"],
        "purchase_amount_usd": state["purchase_amount_usd"],
        "required_approver_role": state["required_approver_role"],
        "assessment": state["assessment"],
        "message": "Review the grounded assessment and approve, reject, or escalate.",
    }

    human_response = interrupt(approval_payload)
    decision = str(human_response.get("decision", "")).lower()
    approver_role = human_response.get("approver_role", "")
    approver_id = human_response.get("approver_id", "")
    comment = human_response.get("comment", "")
    role_valid = approver_role == state["required_approver_role"]

    if decision not in {"approve", "reject", "escalate"}:
        decision = "escalate"
        comment = (comment + " Invalid approval decision; escalated.").strip()

    if decision == "approve" and not role_valid:
        decision = "escalate"
        comment = (comment + " Approver did not hold the required role.").strip()

    return {
        "approval_decision": decision,
        "approver_id": approver_id,
        "approver_role": approver_role,
        "approval_comment": comment,
        "route": decision,
        "audit_log": audit_event(
            state,
            "human_approval_checkpoint",
            decision,
            approver_id_hash=stable_hash(approver_id),
            approver_role=approver_role,
            required_role=state["required_approver_role"],
            role_valid=role_valid,
            comment=comment,
        ),
    }


# Create the final advisory recommendation. This does not execute a purchase.
def finalize_recommendation(state: ProcurementState) -> dict[str, Any]:
    assessment = state["assessment"]
    if assessment.get("recommendation") == "reject":
        status = "REJECTED_BY_POLICY"
    elif state.get("approval_required"):
        status = "APPROVED_RECOMMENDATION"
    else:
        status = "RECOMMENDATION_READY"

    recommendation = {
        "request_id": state["request_id"],
        "status": status,
        "vendor": state["vendor_name"],
        "purchase_amount_usd": state["purchase_amount_usd"],
        "assessment": assessment,
        "approval": {
            "required": state.get("approval_required", False),
            "decision": state.get("approval_decision", "not_required"),
            "approver_role": state.get("approver_role"),
            "comment": state.get("approval_comment"),
        },
        "notice": "This is advisory only. It does not create a purchase order or execute payment.",
    }
    return {
        "final_status": status,
        "final_recommendation": json.dumps(recommendation, indent=2),
        "audit_log": audit_event(state, "finalize_recommendation", status),
    }


# Finalize a human rejection path.
def finalize_rejection(state: ProcurementState) -> dict[str, Any]:
    return {
        "final_status": "REJECTED_BY_APPROVER",
        "final_recommendation": "The purchase recommendation was rejected by the authorized human approver.",
        "audit_log": audit_event(state, "finalize_rejection", "rejected", comment=state.get("approval_comment", "")),
    }


# Finalize any unsafe, unsupported, or escalated path.
def finalize_security_review(state: ProcurementState) -> dict[str, Any]:
    reasons = {
        "injection_signals": state.get("injection_signals", []),
        "content_categories": state.get("content_categories", []),
        "unsupported_claims": state.get("unsupported_claims", []),
        "errors": state.get("errors", []),
    }
    return {
        "final_status": "SECURITY_REVIEW_REQUIRED",
        "final_recommendation": json.dumps(reasons, indent=2),
        "audit_log": audit_event(state, "finalize_security_review", "escalated", reasons=reasons),
    }


# Finalize RBAC denial.
def finalize_access_denied(state: ProcurementState) -> dict[str, Any]:
    return {
        "final_status": "ACCESS_DENIED",
        "final_recommendation": f"The requester is not authorized to perform '{state['requested_action']}'.",
        "audit_log": audit_event(state, "finalize_access_denied", "denied"),
    }


# Finalize invalid input.
def finalize_invalid_request(state: ProcurementState) -> dict[str, Any]:
    return {
        "final_status": "INVALID_REQUEST",
        "final_recommendation": json.dumps({"errors": state.get("validation_errors", [])}, indent=2),
        "audit_log": audit_event(state, "finalize_invalid_request", "rejected"),
    }
