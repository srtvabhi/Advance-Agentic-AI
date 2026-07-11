from config.settings import AZURE_OPENAI_DEPLOYMENT, create_openai_client


client = create_openai_client()


def ask_model(system_message: str, user_message: str) -> str:
    # Sends one simple chat completion request to the configured Foundry model.
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
