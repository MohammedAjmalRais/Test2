from app.models import ResearchResult, TravelContext
from app.services.tavily import TavilyService


class ResearchAgent:
    def __init__(self) -> None:
        self.tavily = TavilyService()

    async def research(self, context: TravelContext) -> tuple[list[ResearchResult], list[str]]:
        if not context.destination:
            return [], ["Destination is required for research"]

        payload = await self.tavily.research_destination(
            destination=context.destination,
            duration_days=context.duration_days,
            preferences=context.preferences,
        )
        if payload.get("error"):
            return [], [str(payload["error"])]

        result = ResearchResult(
            query=payload.get("query", context.destination),
            summary=payload.get("summary", ""),
            highlights=payload.get("highlights", []),
            sources=payload.get("sources", []),
        )
        return [result], []
