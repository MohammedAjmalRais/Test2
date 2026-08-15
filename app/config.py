from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str = ""
    flight_api_key: str = ""
    hotel_api_key: str = ""
    openweather_api_key: str = ""
    tavily_api_key: str = ""
    aviationstack_api_key: str = ""

    gemini_model: str = "gemini-3.5-flash"

    serpapi_base_url: str = "https://serpapi.com/search.json"
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    aviationstack_base_url: str = "http://api.aviationstack.com/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
