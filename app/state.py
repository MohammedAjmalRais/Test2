import operator
from typing import Annotated, Any, TypedDict

from app.models import (
    BudgetEstimate,
    FlightOption,
    HotelOption,
    ResearchResult,
    TravelContext,
    WeatherForecast,
)


class TravelState(TypedDict, total=False):
    user_request: str
    clarification_response: str | None
    prior_context: dict[str, Any] | None

    travel_context: TravelContext
    missing_fields: list[str]
    clarification_question: str | None
    needs_clarification: bool

    flights: list[FlightOption]
    hotels: list[HotelOption]
    weather: WeatherForecast | None
    research: list[ResearchResult]
    budget: BudgetEstimate | None
    itinerary: str | None

    errors: Annotated[list[str], operator.add]
    status: str
    message: str
