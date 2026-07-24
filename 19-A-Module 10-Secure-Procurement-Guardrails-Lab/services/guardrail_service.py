import re


PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"),
    "payment_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "national_id": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}

INJECTION_PATTERNS = {
    "ignore_instructions": re.compile(
        r"ignore (?:all |any )?(?:previous|prior|system) instructions",
        re.IGNORECASE,
    ),
    "reveal_prompt": re.compile(
        r"(?:reveal|show|print|repeat).{0,30}(?:system prompt|hidden instructions|developer message)",
        re.IGNORECASE,
    ),
    "role_override": re.compile(
        r"(?:you are now|act as|pretend to be).{0,40}(?:administrator|manager|system|unrestricted)",
        re.IGNORECASE,
    ),
    "approval_bypass": re.compile(
        r"(?:skip|bypass|disable|avoid).{0,30}(?:approval|guardrail|security|policy|review)",
        re.IGNORECASE,
    ),
    "tool_instruction": re.compile(
        r"(?:execute|run|call).{0,30}(?:tool|function|command|shell|sql)",
        re.IGNORECASE,
    ),
}

CONTENT_PATTERNS = {
    "credential_request": re.compile(r"(?:password|api key|secret token|authentication code)", re.IGNORECASE),
    "financial_account_data": re.compile(r"(?:bank account|routing number|payment card)", re.IGNORECASE),
    "malware_or_exploit": re.compile(r"(?:malware|ransomware|exploit payload|steal credentials)", re.IGNORECASE),
}


# Return labels for every pattern found in the input text.
def detect_patterns(text: str, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    return [label for label, pattern in patterns.items() if pattern.search(text)]


# Redact basic PII before the proposal is sent to the model.
def redact_pii(text: str) -> tuple[str, list[str]]:
    redacted = text
    detected: list[str] = []

    for label, pattern in PII_PATTERNS.items():
        if pattern.search(redacted):
            detected.append(label)
            redacted = pattern.sub(f"[REDACTED_{label.upper()}]", redacted)

    return redacted, detected
