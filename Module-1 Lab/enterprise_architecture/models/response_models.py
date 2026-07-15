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

