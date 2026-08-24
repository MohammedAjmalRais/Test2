import asyncio
from app.agents.orchestrator import OrchestratorAgent

async def main():
    o = OrchestratorAgent()
    res = await o.analyze('Plan a 3 day trip to Paris.', None, None)
    print(res.travel_context)

if __name__ == "__main__":
    asyncio.run(main())
