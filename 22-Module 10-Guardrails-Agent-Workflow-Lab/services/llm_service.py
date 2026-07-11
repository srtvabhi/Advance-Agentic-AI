from config.settings import create_openai_client, get_model_name


def ask_model(system_prompt: str, user_prompt: str) -> str:
    # Sends one chat completion request to the configured Azure AI Foundry model.
    client = create_openai_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
