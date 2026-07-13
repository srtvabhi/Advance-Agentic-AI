# 1- OpenAI Agent SDK-Enterprise-Agent-Lab Reference

This reference explains the Python code used in this lab. It intentionally documents source code only and does not include `.env` secrets.

## Lab Summary

Build an enterprise-style tool-calling agent using the OpenAI Agents SDK.
This lab demonstrates how an agent can use multiple tools to answer user questions and call external services.
The agent can:
- Get the current date and time

## Environment And Setup

This lab should use its own local `.env` file in this folder. Do not rely on a parent/global `.env` file for lab configuration.

Pinned dependencies from `requirements.txt`:

```txt
openai==2.44.0
openai-agents==0.18.0
python-dotenv==1.2.2

```

Typical run pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Python Files

### `agent/enterprise_agent.py`

Role: Agent layer. It defines one or more AI agents and their instructions or orchestration behavior.

Key imports:

- `from agents import Agent`
- `from config.settings import get_model_name`
- `from tools.calculator import calculate`
- `from tools.datetime_tool import get_current_time`
- `from tools.search import web_search`
- `from tools.weather import get_weather`

Functions:

- `create_enterprise_agent()`: Factory/helper function that creates and returns a configured object used by the lab.

Code:

```python
from agents import Agent

from config.settings import get_model_name
from tools.calculator import calculate
from tools.datetime_tool import get_current_time
from tools.search import web_search
from tools.weather import get_weather


# This file defines the enterprise agent.
# The agent can decide which tool to call based on the user's question.


def create_enterprise_agent() -> Agent:
    return Agent(
        name="Enterprise Tool Agent",
        model=get_model_name(),
        instructions=(
            "You are a helpful enterprise assistant. "
            "Use get_current_time for date or time questions. "
            "Use calculate for math questions. "
            "Use get_weather for weather questions. "
            "Use web_search for current or web search questions. "
            "After calling a tool, explain the result clearly."
        ),
        tools=[
            get_current_time,
            calculate,
            get_weather,
            web_search,
        ],
    )


```

### `config/settings.py`

Role: Configuration layer. It loads environment variables and prepares shared settings or clients.

Key imports:

- `import os`
- `from pathlib import Path`
- `from dotenv import load_dotenv`
- `from openai import AsyncOpenAI`
- `from agents import (`

Functions:

- `load_environment()`: Encapsulates reusable logic used by this lab.
- `get_required_setting()`: Retrieves information and returns it in a simple format for the agent or workflow.
- `configure_openai_client()`: Encapsulates reusable logic used by this lab.
- `get_model_name()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
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
# This lab loads only its own .env file.


BASE_DIR = Path(__file__).resolve().parents[1]

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

```

### `main.py`

Role: Application entry point. It wires configuration, agents, tools, services, and the user workflow together.

Key imports:

- `import asyncio`
- `from agent.enterprise_agent import create_enterprise_agent`
- `from config.settings import configure_openai_client`
- `from agents import Runner`

Functions:

- `main()`: Runs the lab from the command line and coordinates the full workflow.

Code:

```python
import asyncio

from agent.enterprise_agent import create_enterprise_agent
from config.settings import configure_openai_client
from agents import Runner


# Enterprise Agent Lab
# This is the application entry point.
# It loads settings, creates the agent, and starts a simple chat loop.


async def main() -> None:
    configure_openai_client()
    agent = create_enterprise_agent()

    print("Enterprise Agent Lab is ready.")
    print("Ask about time, math, weather, or web search.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        result = await Runner.run(agent, question)
        print("\nAgent:", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(main())


```

### `models/response_models.py`

Role: Model layer. It defines data structures used to keep workflow inputs and outputs organized.

Key imports:

- `from dataclasses import dataclass`

Classes:

- `WeatherResponse`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.
- `SearchResult`: Defines a structured object, state model, plugin, service, or agent-related class used by the lab.

Code:

```python
from dataclasses import dataclass


# Models keep API response data organized.
# For this beginner lab, simple dataclasses are enough.


@dataclass
class WeatherResponse:
    city: str
    country: str
    condition: str
    temperature: float
    feels_like: float
    humidity: int

    def to_text(self) -> str:
        return (
            f"Current weather in {self.city}, {self.country}: "
            f"{self.condition}, {self.temperature} C, "
            f"feels like {self.feels_like} C, humidity {self.humidity}%."
        )


@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str

    def to_text(self) -> str:
        return f"{self.title}\n{self.snippet}\n{self.link}"


```

### `services/search_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `import json`
- `from urllib.request import Request, urlopen`
- `from config.settings import SERPER_API_KEY`
- `from models.response_models import SearchResult`

Functions:

- `search_web()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import json
from urllib.request import Request, urlopen

from config.settings import SERPER_API_KEY
from models.response_models import SearchResult


# This service calls Serper for Google-style web search.


def search_web(query: str) -> str:
    request = Request(
        "https://google.serper.dev/search",
        data=json.dumps({"q": query, "num": 3}).encode("utf-8"),
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Web search API error: {exc}"

    organic_results = data.get("organic", [])
    if not organic_results:
        return "No web search results found."

    results = []
    for item in organic_results[:3]:
        results.append(
            SearchResult(
                title=item.get("title", "No title"),
                link=item.get("link", "No link"),
                snippet=item.get("snippet", "No snippet"),
            )
        )

    return "\n\n".join(
        f"{index}. {result.to_text()}"
        for index, result in enumerate(results, start=1)
    )


```

### `services/weather_service.py`

Role: Service layer. It contains business logic or external API integration used by tools and agents.

Key imports:

- `import json`
- `from urllib.parse import urlencode`
- `from urllib.request import urlopen`
- `from config.settings import OPENWEATHER_API_KEY`
- `from models.response_models import WeatherResponse`

Functions:

- `fetch_current_weather()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from config.settings import OPENWEATHER_API_KEY
from models.response_models import WeatherResponse


# Service files contain external API logic.
# This keeps tools simple and easy to read.


def fetch_current_weather(city: str) -> str:
    params = urlencode(
        {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{params}"

    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return f"Weather API error: {exc}"

    weather = WeatherResponse(
        city=data["name"],
        country=data["sys"]["country"],
        condition=data["weather"][0]["description"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
    )

    return weather.to_text()


```

### `tools/calculator.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`

Functions:

- `calculate()`: Encapsulates reusable logic used by this lab.

Code:

```python
from agents import function_tool


# Tool 1: Calculator
# This tool handles simple math expressions.


@function_tool
def calculate(expression: str) -> str:
    """Calculate a basic math expression."""
    print(f"[Tool called: calculate({expression})]")

    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression. Use only numbers and + - * / ( )."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


```

### `tools/datetime_tool.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from datetime import datetime`
- `from agents import function_tool`

Functions:

- `get_current_time()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
from datetime import datetime

from agents import function_tool


# Tool 2: Date and time
# This tool returns the current local system date and time.


@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    print("[Tool called: get_current_time]")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


```

### `tools/search.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`
- `from services.search_service import search_web`

Functions:

- `web_search()`: Encapsulates reusable logic used by this lab.

Code:

```python
from agents import function_tool

from services.search_service import search_web


# Tool 4: Web search
# The tool is small. The API logic lives in services/search_service.py.


@function_tool
def web_search(query: str) -> str:
    """Search the web using Serper and return top results."""
    print(f"[Tool called: web_search({query})]")
    return search_web(query)


```

### `tools/weather.py`

Role: Tool layer. It exposes callable actions that agents or workflows can use.

Key imports:

- `from agents import function_tool`
- `from services.weather_service import fetch_current_weather`

Functions:

- `get_weather()`: Retrieves information and returns it in a simple format for the agent or workflow.

Code:

```python
from agents import function_tool

from services.weather_service import fetch_current_weather


# Tool 3: Weather
# The tool is small. The API logic lives in services/weather_service.py.


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"[Tool called: get_weather({city})]")
    return fetch_current_weather(city)


```


