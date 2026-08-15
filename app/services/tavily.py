from typing import Any

from app.config import get_settings


class TavilyService:
    """Web research for destination attractions and travel tips."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def research_destination(
        self,
        destination: str,
        duration_days: int | None = None,
        preferences: list[str] | None = None,
    ) -> dict[str, Any]:
        if not self.settings.tavily_api_key:
            return {"error": "TAVILY_API_KEY is not configured", "query": destination}

        try:
            from tavily import TavilyClient
        except ImportError:
            return {"error": "tavily-python is not installed", "query": destination}

        prefs = ", ".join(preferences) if preferences else "general sightseeing"
        days = duration_days or 3
        query = (
            f"Best things to do in {destination} for a {days}-day trip. "
            f"Include attractions, neighborhoods, food, and local tips. "
            f"Preferences: {prefs}."
        )

        client = TavilyClient(api_key=self.settings.tavily_api_key)
        result = client.search(
            query=query,
            search_depth="advanced",
            max_results=6,
            include_answer=True,
        )

        highlights: list[str] = []
        sources: list[dict[str, str]] = []
        for item in result.get("results", []):
            title = item.get("title", "")
            snippet = item.get("content", "")[:280]
            if snippet:
                highlights.append(f"{title}: {snippet}")
            sources.append(
                {
                    "title": title,
                    "url": item.get("url", ""),
                }
            )

        return {
            "query": query,
            "summary": result.get("answer") or "",
            "highlights": highlights[:8],
            "sources": sources,
        }
