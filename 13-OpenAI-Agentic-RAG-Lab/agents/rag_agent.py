from config.settings import get_chat_model


def select_data_domain(client, question: str) -> str:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You route business questions to one data domain. "
                    "Return only one word: HR, Sales, Marketing, or All. "
                    "HR is for employee policy, travel, approval, reimbursement, and people questions. "
                    "Sales is for revenue, pipeline, region, product sales, win rate, and deal risks. "
                    "Marketing is for campaigns, audience, messaging, demand generation, and adoption. "
                    "Use All only when the question clearly needs multiple departments."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    selected = (response.choices[0].message.content or "All").strip()
    for domain in ["HR", "Sales", "Marketing", "All"]:
        if domain.lower() in selected.lower():
            return domain
    return "All"


def create_retrieval_plan(client, question: str, selected_domain: str) -> str:
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a retrieval planner. Create a short plan for answering "
                    "the question from enterprise HR, Sales, and Marketing data. "
                    "Mention why the selected data domain is useful. Use 3 bullets."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {question}\nSelected data domain: {selected_domain}",
            },
        ],
    )
    return response.choices[0].message.content or ""


def generate_grounded_answer(client, question: str, selected_domain: str, plan: str, retrieved_chunks) -> str:
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
                    "Include short citations and mention which data domain was used."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\nSelected data domain:\n{selected_domain}\n\nRetrieval plan:\n{plan}\n\n"
                    f"Retrieved context:\n{context}\n\nAnswer:"
                ),
            },
        ],
    )
    return response.choices[0].message.content or ""
