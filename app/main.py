from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import get_settings
from app.graph import get_planner
from app.models import TravelPlanRequest, TravelPlanResponse

app = FastAPI(
    title="AI Travel Planner",
    description=(
        "Multi-agent travel planning system powered by LangGraph, SerpAPI, "
        "OpenWeather, Tavily, and Gemini."
    ),
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "gemini_configured": str(bool(settings.google_api_key)),
        "flight_api_configured": str(bool(settings.flight_api_key)),
        "hotel_api_configured": str(bool(settings.hotel_api_key)),
        "openweather_configured": str(bool(settings.openweather_api_key)),
        "tavily_configured": str(bool(settings.tavily_api_key)),
    }


@app.post("/plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest) -> TravelPlanResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Travel request message is required.")

    settings = get_settings()
    if not settings.google_api_key:
        raise HTTPException(
            status_code=503,
            detail="GOOGLE_API_KEY is not configured. Add it to your .env file.",
        )

    planner = get_planner()
    return await planner.run(request)
