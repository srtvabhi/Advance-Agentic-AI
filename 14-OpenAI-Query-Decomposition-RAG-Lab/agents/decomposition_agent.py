from config.settings import get_chat_model


def decompose_question(client, question: str) -> list[str]:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "Break the user question into 3 focused retrieval sub-questions. "
                    "Return only the sub-questions, one per line, without numbering."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    content = response.choices[0].message.content or ""
    return [line.strip(" -1234567890.") for line in content.splitlines() if line.strip()]


def synthesize_answer(client, question: str, sub_questions: list[str], retrieved_chunks) -> str:
    context = "\n\n".join(
        f"Sub-question: {chunk.sub_question}\nSource: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a RAG synthesis agent. Combine evidence from multiple "
                    "retrieval sub-questions. Cite the PDF sources."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original question:\n{question}\n\nSub-questions:\n{sub_questions}\n\n"
                    f"Retrieved evidence:\n{context}\n\nFinal answer:"
                ),
            },
        ],
    )
    return response.choices[0].message.content or ""
