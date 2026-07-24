APPROVAL_THRESHOLDS = {
    "manager_approval_usd": 25_000,
    "compliance_review_usd": 100_000,
}


# Decide whether procurement manager or compliance officer approval is required.
def get_required_approver(amount: float, risk_level: str, recommendation: str) -> str:
    if amount >= APPROVAL_THRESHOLDS["compliance_review_usd"] or risk_level == "critical":
        return "compliance_officer"

    if amount >= APPROVAL_THRESHOLDS["manager_approval_usd"]:
        return "procurement_manager"

    return ""
