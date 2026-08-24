import json

from app.models import BudgetEstimate, FlightOption, HotelOption, ResearchResult, TravelContext, WeatherForecast
from app.services.gemini import generate_json, generate_text


BUDGET_SYSTEM = """You estimate trip budgets using provided real-world flight and hotel data.
Treat prices as estimates, not guarantees. Return JSON:
{
  "flights": number|null,
  "accommodation": number|null,
  "activities": number|null,
  "food": number|null,
  "local_transport": number|null,
  "total": number|null,
  "currency": "INR",
  "notes": string,
  "breakdown": object
}
"""


ITINERARY_SYSTEM = """You create practical, personalized day-by-day travel itineraries.
Use flights, hotels, weather, research, budget, and user preferences.
Be specific but realistic about timing, neighborhoods, and travel time.

CRITICAL Formatting Rules:
- Write in rich, beautifully formatted Markdown.
- Use primary heading (#) for the main title, e.g., "# Your Travel Itinerary".
- Use secondary headings (##) for main sections: "## Trip Overview", "## Recommended Flight & Hotel Picks", "## Day-by-Day Itinerary", "## Practical Tips".
- Format each day's heading as a secondary heading, e.g., "## Day 1: Arrival & Exploration".
- Use third-level headings (###) for day segments, e.g., "### Morning", "### Afternoon", "### Evening".
- Use bold text (**word**) for emphasis, key times, locations, names, and pricing.
- Use bullet points (- or *) to cleanly structure list items like flights, hotel options, and tips.
- Leave double blank lines (\n\n) between headings, sections, list items, and paragraphs to ensure the reader has clear breathing room.
- CRITICAL: You MUST explicitly list the recommended flights and hotels in your text response, including their names and prices."""


class ItineraryAgent:
    async def estimate_budget(
        self,
        context: TravelContext,
        flights: list[FlightOption],
        hotels: list[HotelOption],
    ) -> BudgetEstimate:
        prompt = f"""Travel context:
{context.model_dump_json()}

Flights:
{json.dumps([f.model_dump(exclude={'raw'}) for f in flights], indent=2)}

Hotels:
{json.dumps([h.model_dump(exclude={'raw'}) for h in hotels], indent=2)}

Estimate a reasonable total trip budget."""

        data = await generate_json(prompt, system=BUDGET_SYSTEM)
        return BudgetEstimate.model_validate(data)

    async def generate_itinerary(
        self,
        context: TravelContext,
        flights: list[FlightOption],
        hotels: list[HotelOption],
        weather: WeatherForecast | None,
        research: list[ResearchResult],
        budget: BudgetEstimate | None,
        user_request: str,
    ) -> str:
        weather_block = weather.model_dump(exclude={"raw"}) if weather else {}
        research_block = [r.model_dump() for r in research]
        budget_block = budget.model_dump() if budget else {}

        prompt = f"""Original user request:
{user_request}

Travel context:
{context.model_dump_json()}

Selected flight options:
{json.dumps([f.model_dump(exclude={'raw'}) for f in flights[:3]], indent=2)}

Selected hotel options:
{json.dumps([h.model_dump(exclude={'raw'}) for h in hotels[:3]], indent=2)}

Weather:
{json.dumps(weather_block, indent=2)}

Destination research:
{json.dumps(research_block, indent=2)}

Budget estimate:
{json.dumps(budget_block, indent=2)}

Create a personalized itinerary with:
1. Trip overview
2. Recommended flight and hotel picks with rationale
3. Day-by-day plan aligned with weather and interests
4. Budget summary (estimate)
5. Practical tips
"""

        return await generate_text(prompt, system=ITINERARY_SYSTEM)
