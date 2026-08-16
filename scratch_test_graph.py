import asyncio
from app.graph import get_planner
from app.models import TravelPlanRequest

async def main():
    planner = get_planner()
    req = TravelPlanRequest(message='Plan a 3-day trip from Hyderabad to Dubai for 1 person')
    res = await planner.run(req)
    print("STATUS:", res.status)
    print("FLIGHTS:", len(res.flights) if res.flights else 0)
    print("ERRORS:", res.errors)

if __name__ == "__main__":
    asyncio.run(main())
