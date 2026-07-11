def summarize_telemetry(telemetry: list[dict]) -> str:
    # Creates a simple local telemetry summary from all workflow steps.
    total_latency = sum(item["latency_ms"] for item in telemetry)
    total_tokens = sum(item["total_tokens"] for item in telemetry)
    prompt_tokens = sum(item["prompt_tokens"] for item in telemetry)
    completion_tokens = sum(item["completion_tokens"] for item in telemetry)

    return (
        f"Steps monitored: {len(telemetry)}\n"
        f"Total latency: {round(total_latency, 2)} ms\n"
        f"Total tokens: {total_tokens}\n"
        f"Prompt tokens: {prompt_tokens}\n"
        f"Completion tokens: {completion_tokens}"
    )
