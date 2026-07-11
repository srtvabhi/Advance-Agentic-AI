import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    # Loads this lab's local environment settings.
    load_dotenv(BASE_DIR / ".env", override=True)


def configure_langsmith() -> bool:
    # Enables LangSmith tracing only when students provide their own key.
    load_environment()
    api_key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    tracing_requested = os.environ.get("LANGSMITH_TRACING", "false").lower() == "true"
    enabled = bool(api_key and tracing_requested)
    os.environ["LANGSMITH_TRACING"] = "true" if enabled else "false"
    return enabled


def get_required_setting(name: str) -> str:
    # Reads a required local setting.
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
    # Returns the configured Foundry chat deployment.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")
