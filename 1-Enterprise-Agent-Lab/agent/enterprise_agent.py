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

