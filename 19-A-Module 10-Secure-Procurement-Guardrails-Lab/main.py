import json
import re
import uuid

from langgraph.types import Command

from config.settings import load_environment
from graphs.procurement_graph import build_procurement_graph
from models.procurement_models import ProcurementState


# Business rule:
# Every procurement request must have a purchase amount because approval routing
# depends on thresholds such as USD 25,000 and USD 100,000.
def extract_amount(prompt: str) -> float:
    match = re.search(r"(?:usd|\$)?\s*([0-9][0-9,]*(?:\.\d+)?)", prompt, flags=re.IGNORECASE)
    if not match:
        return 10000
    return float(match.group(1).replace(",", ""))


# Business rule:
# The requester role controls what action the user is allowed to perform.
# If no role is mentioned, the lab treats the user as a procurement analyst.
def infer_requester_role(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "compliance officer" in prompt_lower:
        return "compliance_officer"
    if "procurement manager" in prompt_lower:
        return "procurement_manager"
    if "employee" in prompt_lower:
        return "employee"
    return "procurement_analyst"


# Business rule:
# Reviewing vendor risk is allowed for procurement users, but approving a
# purchase is a protected action and must go through RBAC checks.
def infer_requested_action(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "approve" in prompt_lower and "purchase" in prompt_lower:
        return "approve_purchase"
    if "submit" in prompt_lower:
        return "submit_vendor_request"
    return "review_vendor_risk"


# Business rule:
# Data classification changes the risk posture. Confidential requests need
# stronger review than public or internal requests.
def infer_data_classification(prompt: str) -> str:
    prompt_lower = prompt.lower()
    explicit_match = re.search(
        r"data classification(?: is|:)\s*(public|internal|confidential)",
        prompt_lower,
    )
    if explicit_match:
        return explicit_match.group(1)

    if "confidential" in prompt_lower:
        return "confidential"
    if "public" in prompt_lower:
        return "public"
    return "internal"


# Business rule:
# Vendor name is mandatory because the workflow must check vendor risk,
# prohibited-vendor policy, and produce an auditable recommendation.
def extract_vendor_name(prompt: str) -> str:
    patterns = [
        r"vendor(?: name)?(?: is|:)\s*([^.\n]+)",
        r"from\s+([^.\n]+)",
        r"with\s+([^.\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .")
    return "Vendor From User Prompt"


# Business rule:
# The learner enters one natural-language request, but the enterprise workflow
# needs structured fields so each guardrail and policy node can make decisions.
def build_request_from_prompt(prompt: str) -> ProcurementState:
    return {
        "request_id": "REQ-CUSTOM-" + uuid.uuid4().hex[:8],
        "requester_id": "learner-001",
        "requester_role": infer_requester_role(prompt),
        "requested_action": infer_requested_action(prompt),
        "vendor_name": extract_vendor_name(prompt),
        "proposal_text": prompt,
        "purchase_amount_usd": extract_amount(prompt),
        "data_classification": infer_data_classification(prompt),
        "audit_log": [],
        "errors": [],
    }


# Business rule:
# Every procurement review must end with a clear final status, recommendation,
# and audit trail so the decision is explainable and traceable.
def print_result(result: dict) -> None:
    print("\nFinal status:", result.get("final_status"))
    print("\nFinal recommendation:")
    print(result.get("final_recommendation"))

    print("\nAudit trail:")
    for event in result.get("audit_log", []):
        print(f"- {event['node']}: {event['decision']}")


# Business rule:
# Show inferred fields before running the workflow so learners can verify that
# the request was interpreted correctly.
def print_inferred_request(request: ProcurementState) -> None:
    print("\nInferred request:")
    print("Requester role:", request["requester_role"])
    print("Requested action:", request["requested_action"])
    print("Vendor:", request["vendor_name"])
    print("Purchase amount USD:", request["purchase_amount_usd"])
    print("Data classification:", request["data_classification"])


# Business rule:
# The graph runs all guardrails first. If the purchase amount or risk requires
# human approval, the workflow pauses and resumes only after an approver responds.
def run_request(request: ProcurementState) -> None:
    workflow = build_procurement_graph()
    config = {"configurable": {"thread_id": request["request_id"]}}
    result = workflow.invoke(request, config=config)

    if "__interrupt__" in result:
        approval_payload = result["__interrupt__"][0].value
        print("\nHuman approval required:")
        print(json.dumps(approval_payload, indent=2))

        decision = input("\nDecision approve/reject/escalate: ").strip().lower() or "approve"
        approver_role = input("Approver role: ").strip() or approval_payload["required_approver_role"]
        approver_id = input("Approver ID: ").strip() or "approver-001"
        comment = input("Approval comment: ").strip() or "Approved for lab demonstration."

        result = workflow.invoke(
            Command(
                resume={
                    "decision": decision,
                    "approver_id": approver_id,
                    "approver_role": approver_role,
                    "comment": comment,
                }
            ),
            config=config,
        )

    print_result(result)


# Business rule:
# Participants should be able to test multiple procurement scenarios in one
# session and exit only when they type quit or exit.
def main() -> None:
    load_environment()
    print("Lab 19-A: Secure Procurement Guardrails and Human Approval Workflow")
    print("Enter one procurement request prompt. Type 'quit' to stop.")

    while True:
        prompt = input("\nProcurement request: ").strip()
        if prompt.lower() in {"quit", "exit"}:
            break
        if not prompt:
            print("Please enter a procurement request, or type 'quit'.")
            continue

        request = build_request_from_prompt(prompt)
        print_inferred_request(request)
        run_request(request)


if __name__ == "__main__":
    main()
