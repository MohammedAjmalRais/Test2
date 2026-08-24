import asyncio
from app.services.hotel_api import HotelApiService
from app.agents.hotel_agent import HotelSearchAgent

async def main():
    agent = HotelSearchAgent()
    payload = await agent.api.search_hotels(
        query="hotels in Tokyo",
        check_in="2026-09-15",
        check_out="2026-09-20",
        adults=1,
        currency="USD"
    )
    hotels = agent._parse_hotels(payload)
    print("Parsed", len(hotels), "hotels")
    if hotels:
        print(hotels[0].model_dump_json())

if __name__ == "__main__":
    asyncio.run(main())
