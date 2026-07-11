import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    # Loads only this lab's local .env file.
    load_dotenv(BASE_DIR / ".env", override=True)


def configure_langsmith() -> bool:
    # Enables LangSmith tracing only when a key is present and tracing is requested.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required environment setting.
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_openai_client() -> OpenAI:
    # Creates an OpenAI-compatible client for Azure AI Foundry.
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def get_model_name() -> str:
    # Returns the configured Foundry chat deployment name.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")
