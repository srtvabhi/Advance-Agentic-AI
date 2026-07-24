ACTION_PERMISSIONS: dict[str, set[str]] = {
    "submit_vendor_request": {
        "employee",
        "procurement_analyst",
        "procurement_manager",
        "compliance_officer",
    },
    "review_vendor_risk": {
        "procurement_analyst",
        "procurement_manager",
        "compliance_officer",
    },
    "approve_purchase": {
        "procurement_manager",
    },
    "approve_compliance_exception": {
        "compliance_officer",
    },
}


# Check whether the authenticated requester role can perform the requested action.
def is_authorized(role: str, action: str) -> bool:
    return role in ACTION_PERMISSIONS.get(action, set())
