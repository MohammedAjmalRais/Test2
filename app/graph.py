import asyncio
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.flight_agent import FlightSearchAgent
from app.agents.hotel_agent import HotelSearchAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.orchestrator import OrchestratorAgent
from app.agents.research_agent import ResearchAgent
from app.agents.weather_agent import WeatherAgent
from app.models import TravelContext, TravelPlanRequest, TravelPlanResponse
from app.state import TravelState


class TravelPlannerGraph:
    """LangGraph workflow coordinating specialized travel-planning agents."""

    def __init__(self) -> None:
        self.orchestrator = OrchestratorAgent()
        self.flight_agent = FlightSearchAgent()
        self.hotel_agent = HotelSearchAgent()
        self.weather_agent = WeatherAgent()
        self.research_agent = ResearchAgent()
        self.itinerary_agent = ItineraryAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(TravelState)

        builder.add_node("orchestrate", self._orchestrate)
        builder.add_node("gather_data", self._gather_data)
        builder.add_node("synthesize", self._synthesize)

        builder.add_edge(START, "orchestrate")
        builder.add_conditional_edges(
            "orchestrate",
            self._route_after_orchestration,
            {
                "clarify": END,
                "continue": "gather_data",
            },
        )
        builder.add_edge("gather_data", "synthesize")
        builder.add_edge("synthesize", END)

        return builder.compile()

    async def _orchestrate(self, state: TravelState) -> dict[str, Any]:
        prior = None
        if state.get("prior_context"):
            prior = TravelContext.model_validate(state["prior_context"])
        elif state.get("travel_context"):
            prior = state["travel_context"]

        result = await self.orchestrator.analyze(
            user_request=state["user_request"],
            prior_context=prior,
            clarification_response=state.get("clarification_response"),
        )

        needs = self.orchestrator.needs_clarification(result)
        return {
            "travel_context": result.travel_context,
            "missing_fields": result.missing_fields,
            "clarification_question": result.clarification_question,
            "needs_clarification": needs,
            "status": "needs_clarification" if needs else "in_progress",
            "message": result.reasoning,
            "errors": [],
        }

    @staticmethod
    def _route_after_orchestration(state: TravelState) -> str:
        if state.get("needs_clarification"):
            return "clarify"
        return "continue"

    async def _gather_data(self, state: TravelState) -> dict[str, Any]:
        context = state["travel_context"]
        errors: list[str] = []

        flight_task = self.flight_agent.search(context)
        hotel_task = self.hotel_agent.search(context)
        weather_task = self.weather_agent.fetch(context)
        research_task = self.research_agent.research(context)

        (
            (flights, flight_errors),
            (hotels, hotel_errors),
            (weather, weather_errors),
            (research, research_errors),
        ) = await asyncio.gather(flight_task, hotel_task, weather_task, research_task)

        errors.extend(flight_errors + hotel_errors + weather_errors + research_errors)

        return {
            "flights": flights,
            "hotels": hotels,
            "weather": weather,
            "research": research,
            "errors": errors,
        }

    async def _synthesize(self, state: TravelState) -> dict[str, Any]:
        context = state["travel_context"]
        flights = state.get("flights") or []
        hotels = state.get("hotels") or []
        weather = state.get("weather")
        research = state.get("research") or []

        budget = await self.itinerary_agent.estimate_budget(context, flights, hotels)
        itinerary = await self.itinerary_agent.generate_itinerary(
            context=context,
            flights=flights,
            hotels=hotels,
            weather=weather,
            research=research,
            budget=budget,
            user_request=state["user_request"],
        )

        return {
            "budget": budget,
            "itinerary": itinerary,
            "status": "complete",
            "message": "Your personalized travel plan is ready.",
        }

    async def run(self, request: TravelPlanRequest) -> TravelPlanResponse:
        initial: TravelState = {
            "user_request": request.message,
            "clarification_response": request.clarification_response,
            "prior_context": request.session_context,
            "errors": [],
        }

        try:
            final = await self.graph.ainvoke(initial)
        except Exception as exc:  # pragma: no cover
            import traceback
            traceback.print_exc()
            return TravelPlanResponse(
                status="error",
                message="Travel planning failed.",
                errors=[str(exc)],
            )

        status = final.get("status", "error")
        if status == "needs_clarification":
            ctx = final.get("travel_context")
            return TravelPlanResponse(
                status="needs_clarification",
                message=final.get("message", "More information is needed."),
                clarification_question=final.get("clarification_question"),
                travel_context=ctx,
                session_context=ctx.model_dump() if ctx else request.session_context,
                errors=final.get("errors") or [],
            )

        return TravelPlanResponse(
            status="complete",
            message=final.get("message", "Travel plan generated."),
            travel_context=final.get("travel_context"),
            flights=final.get("flights") or [],
            hotels=final.get("hotels") or [],
            weather=final.get("weather"),
            research=final.get("research") or [],
            budget=final.get("budget"),
            itinerary=final.get("itinerary"),
            errors=final.get("errors") or [],
        )


_planner: TravelPlannerGraph | None = None


def get_planner() -> TravelPlannerGraph:
    global _planner
    if _planner is None:
        _planner = TravelPlannerGraph()
    return _planner
