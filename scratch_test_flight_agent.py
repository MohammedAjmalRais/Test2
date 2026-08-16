import asyncio
import json
from app.agents.flight_agent import FlightSearchAgent
from app.models import TravelContext

async def main():
    agent = FlightSearchAgent()
    ctx = TravelContext(
        origin="Hyderabad",
        destination="Dubai",
        departure_date="2026-09-15",
        return_date="2026-09-18",
        travelers=1
    )
    flights, errors = await agent.search(ctx)
    print("ERRORS:", errors)
    print("FLIGHTS:", len(flights))
    if flights:
        print("FIRST FLIGHT:", flights[0].model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())
