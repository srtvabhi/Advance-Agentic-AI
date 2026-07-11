import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
EMBEDDING_MODEL = os.environ.get("Embedding_Model", "text-embedding-3-large")


def create_openai_client() -> OpenAI:
    # Creates an OpenAI-compatible client for Azure AI Foundry endpoint.
    return OpenAI(
        base_url=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
    )
