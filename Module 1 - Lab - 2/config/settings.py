import os
from pathlib import Path

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    """Load only this lab folder's .env file."""
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    """Read a required environment value."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def configure_openai_client() -> None:
    """Configure the OpenAI Agents SDK with Azure OpenAI Foundry."""
    load_environment()

    client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )

    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


def get_model_name() -> str:
    """Return the Azure OpenAI deployment name."""
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")
