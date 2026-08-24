#!/usr/bin/env python3
"""Interactive CLI for the WandorAI travel planner."""

import asyncio
import sys

from app.graph import get_planner
from app.models import TravelPlanRequest


async def run_cli() -> None:
    print("WandorAI Travel Planner")
    print("Enter a natural-language travel request (or 'quit' to exit).\n")

    session_context = None
    original_request = ""

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        if not original_request:
            original_request = user_input
            request = TravelPlanRequest(message=user_input)
        else:
            request = TravelPlanRequest(
                message=original_request,
                clarification_response=user_input,
                session_context=session_context,
            )

        print("\nPlanning your trip...\n")
        planner = get_planner()
        response = await planner.run(request)

        if response.status == "needs_clarification":
            session_context = response.session_context
            print(f"Assistant: {response.clarification_question or response.message}\n")
            continue

        if response.status == "error":
            print(f"Error: {response.message}")
            for err in response.errors:
                print(f"  - {err}")
            print()
            original_request = ""
            session_context = None
            continue

        print("=" * 60)
        if response.travel_context:
            ctx = response.travel_context
            print(
                f"Trip: {ctx.origin or 'TBD'} → {ctx.destination} | "
                f"{ctx.duration_days} days | {ctx.travelers} traveler(s)"
            )
        if response.budget:
            print(
                f"Estimated budget: {response.budget.currency} "
                f"{response.budget.total or 'N/A'}"
            )
        if response.errors:
            print("\nNotes:")
            for err in response.errors:
                print(f"  - {err}")
        print("=" * 60)
        print(response.itinerary or response.message)
        print("\n")

        original_request = ""
        session_context = None


def main() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()
