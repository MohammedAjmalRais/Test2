# AI-Powered Multi-Agent Travel Planner

An intelligent travel planning assistant that turns a natural-language sentence into a complete, data-informed travel plan. Enter requests like:

- *"I am planning a trip to Tokyo for 4 days"*
- *"Plan a 7-day trip to Paris from Hyderabad with a moderate budget"*

The system extracts travel requirements, gathers real-world data through specialized agents, and produces a personalized itinerary.

## Architecture

```
User request (natural language)
        │
        ▼
┌───────────────────┐
│ Orchestrator Agent│  ← Gemini: extract destination, dates, budget, etc.
└─────────┬─────────┘
          │ LangGraph
          ▼
┌─────────────────────────────────────────────┐
│ Parallel data gathering                     │
│  • Flight Agent   → SerpAPI (Google Flights)│
│  • Hotel Agent    → SerpAPI (Google Hotels) │
│  • Weather Agent  → OpenWeather API         │
│  • Research Agent → Tavily API              │
│  • Airport Service → IATA resolution        │
└─────────┬───────────────────────────────────┘
          ▼
┌───────────────────┐
│ Itinerary Agent   │  ← Gemini: budget + day-by-day plan
└───────────────────┘
```

## Tech stack

| Component | Technology |
|-----------|------------|
| Orchestration | LangGraph |
| Reasoning & NLG | Google Gemini |
| Flights & hotels | SerpAPI |
| Weather | OpenWeather API |
| Destination research | Tavily API |
| Airport codes | `airportsdata` + optional AviationStack |
| API server | FastAPI |

## Setup

1. **Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure API keys**

```bash
copy .env.example .env
```

Edit `.env` and add your keys:

| Variable | Required | Purpose |
|----------|----------|---------|
| `GOOGLE_API_KEY` | Yes | Gemini orchestration & itinerary |
| `SERPAPI_API_KEY` | Recommended | Real flight & hotel search |
| `OPENWEATHER_API_KEY` | Recommended | Destination weather |
| `TAVILY_API_KEY` | Recommended | Destination research |
| `AVIATIONSTACK_API_KEY` | Optional | Extra airport lookup |

## Usage

### CLI (interactive)

```bash
python cli.py
```

### API server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Health check:** `GET http://localhost:8000/health`

**Create a plan:** `POST http://localhost:8000/plan`

```json
{
  "message": "Plan a 7-day trip to Paris from Hyderabad with a moderate budget"
}
```

If information is missing, the API returns `status: "needs_clarification"`. Reply with:

```json
{
  "message": "Plan a 7-day trip to Paris from Hyderabad with a moderate budget",
  "clarification_response": "Departing March 15, 2026",
  "session_context": { "...prior context from first response..." }
}
```

## Project structure

```
app/
├── agents/           # Specialized agents (orchestrator, flights, hotels, etc.)
├── services/         # External API integrations
├── graph.py          # LangGraph workflow
├── models.py         # Pydantic schemas
├── state.py          # LangGraph shared state
└── main.py           # FastAPI application
cli.py                # Interactive CLI entry point
```

## Notes

- Budget figures are **estimates** based on retrieved data, not guaranteed prices.
- Flight search requires a resolvable **origin** city; hotel and weather search require a **destination**.
- Dates may be inferred (~4 weeks out) when duration is provided but dates are not.
- No user authentication or accounts — direct user-to-AI interaction only.

## License

MIT
"# Test2" 
