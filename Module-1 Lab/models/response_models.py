from dataclasses import dataclass


@dataclass
class WeatherResponse:
    """Structured weather response returned by the weather service."""

    city: str
    country: str
    description: str
    temperature: float
    humidity: int

    def to_text(self) -> str:
        return (
            f"Current weather in {self.city}, {self.country}: "
            f"{self.description}, {self.temperature} C, humidity {self.humidity}%."
        )


@dataclass
class SearchResult:
    """Structured web search result returned by the search service."""

    title: str
    snippet: str
    link: str

    def to_text(self, index: int) -> str:
        return f"{index}. {self.title}\n{self.snippet}\n{self.link}"
