from typing import Any

from app.models import HotelOption, TravelContext
from app.services.hotel_api import HotelApiService

class HotelSearchAgent:
    def __init__(self) -> None:
        self.api = HotelApiService()

    async def search(self, context: TravelContext) -> tuple[list[HotelOption], list[str]]:
        errors: list[str] = []
        if not context.destination:
            return [], ["Destination is required for hotel search"]
        if not context.departure_date or not context.return_date:
            return [], ["Check-in and check-out dates are required for hotel search"]

        import re
        def format_date(d: str) -> str:
            if re.match(r"^\d{2}-\d{2}-\d{4}$", d):
                parts = d.split('-')
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
            return d
            
        check_in = format_date(context.departure_date)
        check_out = format_date(context.return_date)

        query = f"hotels in {context.destination}"
        try:
            payload = await self.api.search_hotels(
                query=query,
                check_in=check_in,
                check_out=check_out,
                adults=context.travelers,
                currency=context.currency,
            )
        except Exception as e:
            errors.append(f"Hotel search failed: {str(e)}")
            return [], errors

        if payload.get("error"):
            errors.append(str(payload["error"]))
            return [], errors

        hotels = self._parse_hotels(payload)
        return hotels[:5], errors

    def _parse_hotels(self, payload: dict[str, Any]) -> list[HotelOption]:
        properties = payload.get("properties") or payload.get("hotels") or []
        options: list[HotelOption] = []
        for item in properties:
            rate = item.get("rate_per_night") or {}
            total = item.get("total_rate") or {}
            options.append(
                HotelOption(
                    name=item.get("name"),
                    location=item.get("location") or item.get("address"),
                    price_per_night=self._extract_price(rate),
                    total_price=self._extract_price(total),
                    rating=item.get("overall_rating") or item.get("rating"),
                    review_count=item.get("reviews") or item.get("review_count"),
                    amenities=item.get("amenities") or [],
                    booking_link=item.get("link"),
                    raw=item,
                )
            )
        return options

    @staticmethod
    def _extract_price(value: Any) -> float | None:
        if isinstance(value, dict):
            extracted = value.get("extracted_lowest") or value.get("lowest")
            return float(extracted) if extracted is not None else None
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                return None
        return None
