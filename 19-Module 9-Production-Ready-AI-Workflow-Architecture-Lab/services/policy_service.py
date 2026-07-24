import re


UNSAFE_RESPONSE_PATTERNS = [
    r"\bsend (?:me|us) your password\b",
    r"\bshare your authentication code\b",
    r"\bguaranteed refund\b",
    r"\bguaranteed resolution\b",
    r"\bdefinitely restored by\b",
]


# Check the generated draft response before it can be sent automatically.
def check_response_policy(response: str) -> tuple[bool, str]:
    violations = [
        pattern
        for pattern in UNSAFE_RESPONSE_PATTERNS
        if re.search(pattern, response, flags=re.IGNORECASE)
    ]

    if not response.strip():
        return False, "Draft response is empty."
    if violations:
        return False, f"Unsafe response pattern found: {violations}"
    return True, "Draft passed deterministic policy checks."
