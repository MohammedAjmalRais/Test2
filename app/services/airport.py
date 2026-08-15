from typing import Any

import httpx

try:
    import airportsdata
except ImportError:  # pragma: no cover
    airportsdata = None  # type: ignore[assignment]

from app.config import get_settings


class AirportService:
    """Resolve city names to IATA codes and decode codes to readable names."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._iata_index: dict[str, dict[str, str]] = {}
        if airportsdata:
            for code, info in airportsdata.load("IATA").items():
                self._iata_index[code.upper()] = {
                    "name": info.get("name", code),
                    "city": info.get("city", ""),
                    "country": info.get("country", ""),
                }

    def iata_to_label(self, code: str) -> str:
        code = code.strip().upper()
        info = self._iata_index.get(code)
        if not info:
            return code
        city = info.get("city") or ""
        name = info.get("name") or code
        if city and city.lower() not in name.lower():
            return f"{name} ({city}) [{code}]"
        return f"{name} [{code}]"

    def _search_local(self, location: str, limit: int = 5) -> list[dict[str, str]]:
        if not self._iata_index:
            return []
        needle = location.strip().lower()
        matches: list[tuple[int, dict[str, str]]] = []
        for code, info in self._iata_index.items():
            city = (info.get("city") or "").lower()
            name = (info.get("name") or "").lower()
            country = (info.get("country") or "").lower()
            score = 0
            if needle == city or needle == name:
                score = 100
            elif needle in city or needle in name:
                score = 80
            elif city.startswith(needle) or name.startswith(needle):
                score = 60
            elif needle in country:
                score = 20
            if score:
                matches.append(
                    (
                        score,
                        {
                            "iata": code,
                            "name": info.get("name", code),
                            "city": info.get("city", ""),
                            "country": info.get("country", ""),
                        },
                    )
                )
        matches.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in matches[:limit]]

    async def _search_aviationstack(self, location: str) -> list[dict[str, str]]:
        if not self.settings.aviationstack_api_key:
            return []
        params = {
            "access_key": self.settings.aviationstack_api_key,
            "search": location,
            "limit": 5,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.settings.aviationstack_base_url}/autocomplete",
                params=params,
            )
            if response.status_code != 200:
                return []
            payload = response.json()
        results: list[dict[str, str]] = []
        for item in payload.get("data", []):
            code = item.get("iata_code") or item.get("airport_iata") or ""
            if not code:
                continue
            results.append(
                {
                    "iata": code.upper(),
                    "name": item.get("airport_name") or item.get("name") or code,
                    "city": item.get("city_name") or item.get("city") or "",
                    "country": item.get("country_name") or item.get("country") or "",
                }
            )
        return results

    async def resolve_to_iata(self, location: str) -> str | None:
        """Convert a human-readable location to the best matching IATA code."""
        if not location:
            return None
        if len(location.strip()) == 3 and location.strip().isalpha():
            return location.strip().upper()

        local = self._search_local(location, limit=1)
        if local:
            return local[0]["iata"]

        remote = await self._search_aviationstack(location)
        if remote:
            return remote[0]["iata"]
        return None

    async def lookup(self, location: str) -> list[dict[str, str]]:
        local = self._search_local(location)
        if local:
            return local
        return await self._search_aviationstack(location)

    def enrich_flight_airports(self, flight: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(flight)
        for key in ("departure_airport", "arrival_airport"):
            code = enriched.get(key)
            if code and len(str(code)) == 3:
                enriched[f"{key}_label"] = self.iata_to_label(str(code))
        return enriched
