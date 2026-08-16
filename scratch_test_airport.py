import asyncio
from app.services.airport import AirportService

async def main():
    service = AirportService()
    print("HYDERABAD:", await service.resolve_to_iata("Hyderabad"))
    print("DUBAI:", await service.resolve_to_iata("Dubai"))

if __name__ == "__main__":
    asyncio.run(main())
