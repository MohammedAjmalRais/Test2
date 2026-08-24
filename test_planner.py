import asyncio
import sys
from app.graph import get_planner
from app.models import TravelPlanRequest

async def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    planner = get_planner()
    req = TravelPlanRequest(message='plan a trip to Tokyo from 18-08-2026 to 02-09-2026 from Delhi for one traveler.')
    res = await planner.run(req)
    print("STATUS:", res.status)
    print("MESSAGE:", res.message)
    print("ERRORS:", res.errors)
    print("FLIGHTS_LEN:", len(res.flights))
    print("HOTELS_LEN:", len(res.hotels))
    print("HOTELS:", res.hotels)

if __name__ == "__main__":
    asyncio.run(main())
