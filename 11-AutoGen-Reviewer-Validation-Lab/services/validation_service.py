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
