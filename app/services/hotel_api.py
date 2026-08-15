from typing import Any
import httpx
from app.config import get_settings

class HotelApiService:
    """Client for Google Hotels via SerpAPI."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def _search(self, params: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.hotel_api_key:
            return {"error": "HOTEL_API_KEY is not configured"}

        query = {**params, "api_key": self.settings.hotel_api_key}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(self.settings.serpapi_base_url, params=query)
            response.raise_for_status()
            return response.json()

    async def search_hotels(
        self,
        query: str,
        check_in: str,
        check_out: str,
        adults: int = 1,
        currency: str = "USD",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "engine": "google_hotels",
            "q": query,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": adults,
            "currency": currency,
        }
        return await self._search(params)
