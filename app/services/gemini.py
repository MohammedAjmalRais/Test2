import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.config import get_settings


def _get_client() -> genai.Client:
    settings = get_settings()
    return genai.Client(api_key=settings.google_api_key)


def _extract_json(text: str) -> dict[str, Any]:
    """Extract JSON object from model response."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


async def generate_text(prompt: str, system: str | None = None) -> str:
    settings = get_settings()
    client = _get_client()
    config = types.GenerateContentConfig(
        system_instruction=system or "You are a helpful travel planning assistant.",
    )
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )
    return response.text or ""


async def generate_json(prompt: str, system: str | None = None) -> dict[str, Any]:
    text = await generate_text(
        prompt + "\n\nRespond with valid JSON only, no markdown fences.",
        system=system,
    )
    return _extract_json(text)
