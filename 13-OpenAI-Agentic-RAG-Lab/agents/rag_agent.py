from config.settings import get_chat_model


def create_retrieval_plan(client, question: str) -> str:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a retrieval planner. Create a short plan for answering "
                    "the question from enterprise policy documents. Use 3 bullets."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""


def generate_grounded_answer(client, question: str, plan: str, retrieved_chunks) -> str:
    context = "\n\n".join(
        f"Source: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise RAG assistant. Answer only from the provided context. "
                    "If context is missing, say what is missing. Pay close attention to "
                    "threshold words such as over, under, between, before, and after. "
                    "Include short citations."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\nRetrieval plan:\n{plan}\n\n"
                    f"Retrieved context:\n{context}\n\nAnswer:"
                ),
            },
        ],
    )
    return response.choices[0].message.content or ""
