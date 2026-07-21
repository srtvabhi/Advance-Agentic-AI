import os
from pathlib import Path

from agents import OpenAIProvider, RunConfig
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
HR_DIR = DATA_DIR / "HR"
SALES_DIR = DATA_DIR / "Sales"
MARKETING_DIR = DATA_DIR / "Marketing"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def get_embedding_model() -> str:
    load_environment()
    return (
        os.environ.get("Embedding_Model")
        or os.environ.get("EMBEDDING_MODEL")
        or "text-embedding-3-large"
    )


def get_chat_model() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )


def create_agents_run_config(workflow_name: str) -> RunConfig:
    """Configure the OpenAI Agents SDK to use this lab's Azure endpoint."""
    load_environment()
    async_client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
    provider = OpenAIProvider(openai_client=async_client, use_responses=False)
    return RunConfig(
        model_provider=provider,
        workflow_name=workflow_name,
        tracing_disabled=True,
    )
