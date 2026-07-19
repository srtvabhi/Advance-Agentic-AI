from config.settings import create_openai_client, get_model_name


async def ask_llm(system_prompt: str, user_prompt: str) -> str:
    client = create_openai_client()
    response = await client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""
