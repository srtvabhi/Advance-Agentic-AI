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

