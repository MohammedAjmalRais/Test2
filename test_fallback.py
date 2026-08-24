import asyncio
import os
import logging
from app.services.gemini import generate_text
from app.config import get_settings

logging.basicConfig(level=logging.WARNING)

async def test():
    # Force Gemini model to be an invalid one to trigger error
    settings = get_settings()
    settings.gemini_model = "gemini-invalid-model-1"
    settings.gemini_fallback_models = ["gemini-invalid-model-2"]
    
    # Normally this would fallback to Groq, let's see if it tries and fails since GROQ_API_KEY_FALLBACK is empty
    print("Testing generate_text with invalid Gemini models...")
    try:
        res = await generate_text("Say hello")
        print("Success:", res)
    except Exception as e:
        print("Caught final error as expected:", e)

if __name__ == "__main__":
    asyncio.run(test())
