KNOWLEDGE_BASE = [
    {
        "id": "KB-BILLING-001",
        "category": "billing",
        "text": "For suspected duplicate charges, create a billing case and verify transaction history before discussing refunds.",
    },
    {
        "id": "KB-REFUND-001",
        "category": "billing",
        "text": "Refunds above the automatic threshold require human approval before the customer is promised a refund.",
    },
    {
        "id": "KB-ACCESS-001",
        "category": "account_access",
        "text": "For account access issues, direct customers to the secure password reset process. Never request passwords or one-time codes.",
    },
    {
        "id": "KB-INCIDENT-001",
        "category": "service_incident",
        "text": "For service incidents, provide only confirmed incident identifiers and next update times. Do not promise unconfirmed restoration times.",
    },
    {
        "id": "KB-GENERAL-001",
        "category": "general_support",
        "text": "For general support, acknowledge the request and ask only for the minimum additional information required.",
    },
]


# Retrieve approved knowledge using simple category and keyword scoring.
def retrieve_knowledge(intent: str, subject: str, body: str, top_k: int = 3) -> list[dict]:
    query = f"{subject} {body}".lower()
    ranked = []

    for document in KNOWLEDGE_BASE:
        score = 0
        if document["category"] == intent:
            score += 5
        for word in query.split():
            if len(word) > 3 and word in document["text"].lower():
                score += 1
        ranked.append({**document, "score": score})

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_k]
