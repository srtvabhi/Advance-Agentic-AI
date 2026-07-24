import re


PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"),
    "card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


# Find simple PII patterns in the ticket body.
def find_pii(text: str) -> list[str]:
    return [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]


# Replace PII values before sending ticket text to the model.
def redact_pii(text: str) -> str:
    redacted = text
    for name, pattern in PII_PATTERNS.items():
        redacted = pattern.sub(f"[REDACTED_{name.upper()}]", redacted)
    return redacted
