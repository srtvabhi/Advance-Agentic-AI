import random
import time
from dataclasses import dataclass

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    OpenAI,
    PermissionDeniedError,
    RateLimitError,
)

from config.settings import get_model_target_configs, normalize_endpoint


@dataclass
class ModelTarget:
    name: str
    client: OpenAI
    deployment: str


class AllModelTargetsFailed(RuntimeError):
    def __init__(self, failures: list[dict]) -> None:
        self.failures = failures
        super().__init__("Every configured model target failed.")


TRANSIENT_EXCEPTIONS = (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)

NON_RETRYABLE_EXCEPTIONS = (
    AuthenticationError,
    PermissionDeniedError,
    BadRequestError,
    NotFoundError,
)


# Decide if the model call should be retried.
def is_retryable_exception(exc: Exception) -> bool:
    if isinstance(exc, TRANSIENT_EXCEPTIONS):
        return True
    if isinstance(exc, NON_RETRYABLE_EXCEPTIONS):
        return False
    if isinstance(exc, APIStatusError):
        return exc.status_code in {408, 409, 429} or exc.status_code >= 500
    return False


# Calculate exponential backoff with small random jitter.
def calculate_backoff(attempt: int) -> float:
    base_delay = min(0.5 * (2 ** (attempt - 1)), 4.0)
    jitter = random.uniform(0, base_delay * 0.25)
    return base_delay + jitter


# Call one Azure OpenAI target with explicit retry logic.
def call_single_target_with_retry(
    target: ModelTarget,
    system_prompt: str,
    user_prompt: str,
    max_attempts: int,
) -> tuple[str, dict]:
    failures = []

    for attempt in range(1, max_attempts + 1):
        started = time.perf_counter()
        try:
            response = target.client.chat.completions.create(
                model=target.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            latency_ms = round((time.perf_counter() - started) * 1000, 2)
            return response.choices[0].message.content or "", {
                "target": target.name,
                "deployment": target.deployment,
                "attempt": attempt,
                "retry_count": attempt - 1,
                "latency_ms": latency_ms,
            }
        except Exception as exc:
            retryable = is_retryable_exception(exc)
            failure = {
                "target": target.name,
                "deployment": target.deployment,
                "attempt": attempt,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "retryable": retryable,
            }
            failures.append(failure)

            if not retryable or attempt == max_attempts:
                raise AllModelTargetsFailed(failures)

            time.sleep(calculate_backoff(attempt))

    raise AllModelTargetsFailed(failures)


# Call primary model first. If it is exhausted, activate fallback model.
def call_model_with_fallback(
    system_prompt: str,
    user_prompt: str,
    max_attempts_per_target: int = 3,
) -> tuple[str, dict]:
    all_failures = []

    targets = [
        ModelTarget(
            name=config["name"],
            client=OpenAI(
                base_url=normalize_endpoint(config["endpoint"]),
                api_key=config["api_key"],
                max_retries=0,
                timeout=30.0,
            ),
            deployment=config["deployment"],
        )
        for config in get_model_target_configs()
    ]

    for index, target in enumerate(targets):
        fallback_activated = index > 0
        try:
            output, metadata = call_single_target_with_retry(
                target=target,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_attempts=max_attempts_per_target,
            )
            metadata["fallback_activated"] = fallback_activated
            metadata["previous_failures"] = all_failures
            return output, metadata
        except AllModelTargetsFailed as exc:
            all_failures.extend(exc.failures)

    raise AllModelTargetsFailed(all_failures)
