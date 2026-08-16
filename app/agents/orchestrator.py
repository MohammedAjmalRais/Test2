from datetime import datetime, timedelta
from typing import Any

from app.models import OrchestratorResult, TravelContext
from app.services.gemini import generate_json


ORCHESTRATOR_SYSTEM = """You extract structured travel requirements from natural language.
Return JSON with this shape:
{
  "travel_context": {
    "destination": string|null,
    "origin": string|null,
    "duration_days": integer|null,
    "departure_date": "YYYY-MM-DD"|null,
    "return_date": "YYYY-MM-DD"|null,
    "travelers": integer,
    "budget_preference": "low"|"moderate"|"high"|"luxury"|null,
    "budget_amount": number|null,
    "currency": "INR",
    "preferences": [string],
    "constraints": [string],
    "trip_purpose": string|null,
    "inferred_fields": [string]
  },
  "missing_fields": [string],
  "clarification_question": string|null,
  "confidence": number,
  "reasoning": string
}

Rules:
- Infer reasonable defaults when possible and list them in inferred_fields.
- If duration is given but dates are missing, infer departure_date roughly 4 weeks from today.
- missing_fields should use keys like destination, origin, duration_days, departure_date.
- Ask ONE concise clarification_question only when destination or duration_days cannot be inferred.
- budget_preference can be inferred from phrases like "moderate budget".
- travelers defaults to 1 unless specified.
"""


class OrchestratorAgent:
    async def analyze(
        self,
        user_request: str,
        prior_context: TravelContext | None = None,
        clarification_response: str | None = None,
    ) -> OrchestratorResult:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        context_block = ""
        if prior_context:
            context_block = f"\nExisting context:\n{prior_context.model_dump_json()}\n"
        if clarification_response:
            context_block += f"\nUser clarification:\n{clarification_response}\n"

        prompt = f"""Today's date: {today}
User request: {user_request}
{context_block}
Extract travel requirements and identify missing critical information."""

        data = await generate_json(prompt, system=ORCHESTRATOR_SYSTEM)
        ctx_data = data.get("travel_context", {})
        ctx_data = self._apply_defaults(ctx_data, today)

        return OrchestratorResult(
            travel_context=TravelContext.model_validate(ctx_data),
            missing_fields=data.get("missing_fields", []),
            clarification_question=data.get("clarification_question"),
            confidence=float(data.get("confidence", 0.8)),
            reasoning=data.get("reasoning", ""),
        )

    @staticmethod
    def _apply_defaults(ctx: dict[str, Any], today: str) -> dict[str, Any]:
        if not ctx.get("travelers"):
            ctx["travelers"] = 1
        if not ctx.get("currency"):
            ctx["currency"] = "INR"

        duration = ctx.get("duration_days")
        if duration and not ctx.get("departure_date"):
            base = datetime.strptime(today, "%Y-%m-%d") + timedelta(days=28)
            ctx["departure_date"] = base.strftime("%Y-%m-%d")
            ctx.setdefault("inferred_fields", []).append("departure_date")
        if duration and ctx.get("departure_date") and not ctx.get("return_date"):
            start = datetime.strptime(ctx["departure_date"], "%Y-%m-%d")
            end = start + timedelta(days=max(int(duration) - 1, 0))
            ctx["return_date"] = end.strftime("%Y-%m-%d")
            ctx.setdefault("inferred_fields", []).append("return_date")
        return ctx

    @staticmethod
    def needs_clarification(result: OrchestratorResult) -> bool:
        critical = {"destination", "duration_days"}
        missing_critical = critical.intersection(set(result.missing_fields))
        if missing_critical and result.clarification_question:
            return True
        if not result.travel_context.destination:
            return True
        if not result.travel_context.duration_days:
            return True
        return False
