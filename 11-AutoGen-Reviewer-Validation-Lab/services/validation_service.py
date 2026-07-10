def validate_review(review_text: str) -> str:
    text = review_text.upper()
    if "REVISION_REQUIRED" in text:
        return "REVISION_REQUIRED"
    if "APPROVED" in text:
        return "APPROVED"
    return "REVISION_REQUIRED"
