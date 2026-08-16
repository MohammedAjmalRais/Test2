import asyncio
import os
from dotenv import load_dotenv

from app.services.flight_api import FlightApiService

load_dotenv()

async def main():
    api = FlightApiService()
    res = await api.search_flights('HYD', 'DXB', '2026-09-15', return_date='2026-09-18')
    print("KEYS:", res.keys())
    if "error" in res:
        print("ERROR:", res["error"])
    elif "best_flights" in res:
        print("BEST FLIGHTS:", len(res["best_flights"]))
    elif "other_flights" in res:
        print("OTHER FLIGHTS:", len(res["other_flights"]))
    else:
        print("RES:", res)

asyncio.run(main())
