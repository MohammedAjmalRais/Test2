from datetime import datetime, timedelta
from typing import Any

import httpx

from app.config import get_settings


class OpenWeatherService:
    """Fetch current and forecast weather for a destination."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def _geocode(self, location: str) -> tuple[float, float, str] | None:
        if not self.settings.openweather_api_key:
            return None
        params = {
            "q": location,
            "limit": 1,
            "appid": self.settings.openweather_api_key,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.openweathermap.org/geo/1.0/direct",
                params=params,
            )
            if response.status_code != 200:
                return None
            data = response.json()
        if not data:
            return None
        place = data[0]
        label = place.get("name", location)
        if place.get("country"):
            label = f"{label}, {place['country']}"
        return place["lat"], place["lon"], label

    async def get_forecast(
        self,
        location: str,
        days: int = 5,
    ) -> dict[str, Any]:
        if not self.settings.openweather_api_key:
            return {"error": "OPENWEATHER_API_KEY is not configured"}

        geo = await self._geocode(location)
        if not geo:
            return {"error": f"Could not geocode location: {location}"}

        lat, lon, label = geo
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.settings.openweather_api_key,
            "units": "metric",
            "cnt": min(max(days, 1), 5) * 8,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.settings.openweather_base_url}/forecast",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()

        daily: dict[str, dict[str, Any]] = {}
        for item in payload.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            day_key = dt.strftime("%Y-%m-%d")
            if day_key not in daily:
                daily[day_key] = {
                    "date": day_key,
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item.get("wind", {}).get("speed"),
                }

        ordered_days = sorted(daily.keys())[:days]
        return {
            "location": label,
            "summary": self._build_summary([daily[d] for d in ordered_days]),
            "daily": [daily[d] for d in ordered_days],
            "raw": payload,
        }

    @staticmethod
    def _build_summary(daily: list[dict[str, Any]]) -> str:
        if not daily:
            return "Weather data unavailable."
        temps = [d["temp_max"] for d in daily]
        descriptions = {d["description"] for d in daily}
        return (
            f"Expect highs around {min(temps):.0f}–{max(temps):.0f}°C with "
            f"conditions such as {', '.join(sorted(descriptions))}."
        )

    @staticmethod
    def default_dates(duration_days: int) -> tuple[str, str]:
        start = datetime.utcnow() + timedelta(days=30)
        end = start + timedelta(days=max(duration_days - 1, 0))
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
