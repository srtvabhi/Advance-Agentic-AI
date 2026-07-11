from langsmith import traceable

from config.settings import create_openai_client, get_model_name


@traceable(name="foundry_chat_completion", run_type="llm")
def ask_model(system_prompt: str, user_prompt: str) -> str:
    # Sends one traced chat completion request to Azure AI Foundry.
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
