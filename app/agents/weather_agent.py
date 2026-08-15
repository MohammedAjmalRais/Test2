from app.models import TravelContext, WeatherForecast
from app.services.openweather import OpenWeatherService


class WeatherAgent:
    def __init__(self) -> None:
        self.weather = OpenWeatherService()

    async def fetch(self, context: TravelContext) -> tuple[WeatherForecast | None, list[str]]:
        if not context.destination:
            return None, ["Destination is required for weather lookup"]

        days = context.duration_days or 5
        payload = await self.weather.get_forecast(context.destination, days=days)
        if payload.get("error"):
            return None, [str(payload["error"])]

        forecast = WeatherForecast(
            location=payload.get("location", context.destination),
            summary=payload.get("summary", ""),
            daily=payload.get("daily", []),
            raw=payload.get("raw", {}),
        )
        return forecast, []
