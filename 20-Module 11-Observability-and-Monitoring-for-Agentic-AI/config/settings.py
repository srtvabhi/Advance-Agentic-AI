import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
HR_DIR = DATA_DIR / "HR"
SALES_DIR = DATA_DIR / "Sales"
MARKETING_DIR = DATA_DIR / "Marketing"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
HR_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "hr_knowledge"
SALES_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "sales_knowledge"
MARKETING_VECTOR_STORE_DIR = VECTOR_STORE_DIR / "marketing_knowledge"


def load_environment() -> None:
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        raise FileNotFoundError(
            f"Missing local environment file: {env_file}. "
            "Create this file from .env.example so the lab does not use global environment variables."
        )
    load_dotenv(env_file, override=True)


def configure_langsmith() -> None:
    """Load this lab's LangSmith settings and enable tracing for local runs."""
    load_environment()
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ.setdefault("LANGSMITH_PROJECT", "lab20_abhishek")

    # Older LangSmith integrations still read the LANGCHAIN_* names.
    os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGSMITH_TRACING", "true")
    os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "lab20_abhishek")
    if os.environ.get("LANGSMITH_API_KEY"):
        os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGSMITH_API_KEY"]


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


def create_chat_model() -> ChatOpenAI:
    """Create a LangChain chat model so LangSmith can capture LLM token usage."""
    configure_langsmith()
    return ChatOpenAI(
        model=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
