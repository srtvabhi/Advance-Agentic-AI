import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment() -> None:
    # Loads only this lab's local .env file.
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    # Reads a required environment value and raises a clear error when missing.
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
    # Returns the chat model deployment name from this lab's .env file.
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_embedding_model() -> str:
    # Keeps the embedding model available for governance labs that later add RAG.
    load_environment()
    return os.environ.get("Embedding_Model") or "text-embedding-3-large"
