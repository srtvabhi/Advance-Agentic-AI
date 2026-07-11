import time

from langsmith import traceable

from config.settings import create_openai_client, get_model_name


@traceable(name="monitored_foundry_chat_completion", run_type="llm")
def ask_model_with_metrics(step_name: str, system_prompt: str, user_prompt: str) -> tuple[str, dict]:
    # Calls the model and returns output plus token and latency telemetry.
    client = create_openai_client()
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    usage = response.usage
    metrics = {
        "step": step_name,
        "latency_ms": latency_ms,
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }
    return response.choices[0].message.content or "", metrics
