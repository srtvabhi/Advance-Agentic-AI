import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def normalize_endpoint(endpoint: str) -> str:
    return endpoint.rstrip("/") + "/"


def create_openai_client(endpoint_setting: str = "AZURE_OPENAI_ENDPOINT", key_setting: str = "AZURE_OPENAI_API_KEY") -> OpenAI:
    load_environment()
    return OpenAI(
        base_url=normalize_endpoint(get_required_setting(endpoint_setting)),
        api_key=get_required_setting(key_setting),
        max_retries=0,
        timeout=30.0,
    )


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_model_target_configs() -> list[dict[str, str]]:
    load_environment()
    fallback_endpoint = os.environ.get("AZURE_OPENAI_FALLBACK_ENDPOINT") or get_required_setting("AZURE_OPENAI_ENDPOINT")
    fallback_key = os.environ.get("AZURE_OPENAI_FALLBACK_API_KEY") or get_required_setting("AZURE_OPENAI_API_KEY")
    fallback_deployment = os.environ.get("AZURE_OPENAI_FALLBACK_DEPLOYMENT") or get_required_setting("AZURE_OPENAI_DEPLOYMENT")

    return [
        {
            "name": "primary",
            "endpoint": get_required_setting("AZURE_OPENAI_ENDPOINT"),
            "api_key": get_required_setting("AZURE_OPENAI_API_KEY"),
            "deployment": get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
        },
        {
            "name": "fallback",
            "endpoint": fallback_endpoint,
            "api_key": fallback_key,
            "deployment": fallback_deployment,
        },
    ]


def get_embedding_model() -> str:
    load_environment()
    return os.environ.get("Embedding_Model") or os.environ.get("EMBEDDING_MODEL") or "text-embedding-3-large"
