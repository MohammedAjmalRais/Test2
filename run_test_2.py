import asyncio
from app.graph import get_planner
from app.models import TravelPlanRequest
import json

async def main():
    planner = get_planner()
    # Using the prompt from the UI screenshot without an origin
    req = TravelPlanRequest(message='Plan a 5-day trip to Tokyo next month. I love nature and quiet places.')
    try:
        res = await planner.run(req)
        print("STATUS:", res.status)
        print("ERRORS:", res.errors)
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    asyncio.run(main())
