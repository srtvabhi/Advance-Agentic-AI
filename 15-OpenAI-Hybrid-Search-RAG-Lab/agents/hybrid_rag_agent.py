from config.settings import get_chat_model


def detect_product_filter(question: str) -> str | None:
    lowered = question.lower()
    if "analyticspro" in lowered or "analytics pro" in lowered:
        return "AnalyticsPro"
    if "securepay" in lowered or "secure pay" in lowered:
        return "SecurePay"
    return None


def answer_with_hybrid_context(client, question: str, results) -> str:
    context = "\n\n".join(
        f"Search type: {item.search_type}\nScore: {item.score:.3f}\nSource: {item.citation()}\nContent: {item.text}"
        for item in results
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support RAG assistant. Use the hybrid search context only. "
                    "Explain the answer simply and include citations."
                ),
            },
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nHybrid search context:\n{context}\n\nAnswer:",
            },
        ],
    )
    return response.choices[0].message.content or ""
