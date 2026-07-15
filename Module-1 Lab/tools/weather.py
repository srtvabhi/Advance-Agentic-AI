from agents import function_tool

from services.weather_service import fetch_current_weather


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"[Tool called: get_weather({city})]")
    return fetch_current_weather(city)
