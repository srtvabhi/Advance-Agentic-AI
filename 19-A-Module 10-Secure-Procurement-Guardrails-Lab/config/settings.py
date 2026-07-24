import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]


# Load only this lab folder's .env file so the lab does not depend on the parent environment.
def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


# Read a required environment variable and fail early with a learner-friendly message.
def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


# Azure OpenAI /openai/v1 endpoints should end with one slash for the OpenAI client.
def normalize_endpoint(endpoint: str) -> str:
    return endpoint.rstrip("/") + "/"


# Create the OpenAI client used by policy embeddings and grounded risk assessment.
def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(
        base_url=normalize_endpoint(get_required_setting("AZURE_OPENAI_ENDPOINT")),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
        timeout=30.0,
        max_retries=2,
    )


# Return the Azure AI Foundry chat deployment name.
def get_chat_model() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


# Return the embedding deployment name. The lab accepts both naming styles used in earlier labs.
def get_embedding_model() -> str:
    load_environment()
    return (
        os.environ.get("Embedding_Model")
        or os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
        or os.environ.get("EMBEDDING_MODEL")
        or "text-embedding-3-large"
    )
