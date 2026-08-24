import json
import re
import asyncio
import logging
from typing import Any

from google import genai
from google.genai import types
from groq import AsyncGroq

from app.config import get_settings

logger = logging.getLogger(__name__)


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
    
    models_to_try = [settings.gemini_model] + settings.gemini_fallback_models
    system_instruction = system or "You are a helpful travel planning assistant."
    
    for model in models_to_try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
        )
        
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except Exception as e:
            logger.warning(f"Model {model} failed on first attempt: {e}. Retrying in 4 seconds...")
            await asyncio.sleep(4)
            
            try:
                response = await client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                return response.text or ""
            except Exception as e2:
                logger.warning(f"Model {model} failed on retry: {e2}. Falling back to next model.")
                continue
                
    logger.error("All Gemini models failed. Falling back to Groq.")
    
    if not settings.groq_api_key_fallback:
        raise RuntimeError("All Gemini models failed and GROQ_API_KEY_FALLBACK is not set.")
        
    groq_client = AsyncGroq(api_key=settings.groq_api_key_fallback)
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ]
    
    groq_response = await groq_client.chat.completions.create(
        model=settings.groq_fallback_model,
        messages=messages,
        temperature=0.2,
    )
    
    return groq_response.choices[0].message.content or ""


async def generate_json(prompt: str, system: str | None = None) -> dict[str, Any]:
    text = await generate_text(
        prompt + "\n\nRespond with valid JSON only, no markdown fences.",
        system=system,
    )
    return _extract_json(text)
