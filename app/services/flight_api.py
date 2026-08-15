from typing import Any
import httpx
from app.config import get_settings

class FlightApiService:
    """Client for Google Flights via SerpAPI."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def _search(self, params: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.flight_api_key:
            return {"error": "FLIGHT_API_KEY is not configured"}

        query = {**params, "api_key": self.settings.flight_api_key}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(self.settings.serpapi_base_url, params=query)
            response.raise_for_status()
            return response.json()

    async def search_flights(
        self,
        origin_iata: str,
        destination_iata: str,
        departure_date: str,
        return_date: str | None = None,
        adults: int = 1,
        currency: str = "USD",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "engine": "google_flights",
            "departure_id": origin_iata,
            "arrival_id": destination_iata,
            "outbound_date": departure_date,
            "adults": adults,
            "currency": currency,
            "type": 1 if return_date else 2,
        }
        if return_date:
            params["return_date"] = return_date
        return await self._search(params)
