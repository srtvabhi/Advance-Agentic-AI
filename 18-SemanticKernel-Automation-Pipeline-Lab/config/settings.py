import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SOURCE_DOCS_DIR = DATA_DIR / "source_docs"
PDF_DIR = DATA_DIR / "pdfs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def get_chat_model() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")


def get_embedding_model() -> str:
    load_environment()
    return os.environ.get("Embedding_Model") or os.environ.get("EMBEDDING_MODEL") or "text-embedding-3-large"


def create_openai_client() -> OpenAI:
    load_environment()
    return OpenAI(base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"), api_key=get_required_setting("AZURE_OPENAI_API_KEY"))


def create_kernel() -> Kernel:
    load_environment()
    kernel = Kernel()
    async_client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
    kernel.add_service(
        OpenAIChatCompletion(
            ai_model_id=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
            async_client=async_client,
            service_id="foundry-chat",
        )
    )
    return kernel
