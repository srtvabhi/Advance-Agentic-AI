import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


# This file keeps configuration in one place.
# This merged lab loads the shared Module-1 Lab/.env file.


BASE_DIR = Path(__file__).resolve().parents[2]

OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"
SERPER_API_KEY = "62a1f0bf33831bc01421f5d84c716a66f2c5ba3e"


def load_environment() -> None:
    load_dotenv(BASE_DIR / ".env", override=True)


def get_required_setting(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def configure_openai_client() -> None:
    load_environment()

    client = AsyncOpenAI(
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )

    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


def get_model_name() -> str:
    load_environment()
    return get_required_setting("AZURE_OPENAI_DEPLOYMENT")
