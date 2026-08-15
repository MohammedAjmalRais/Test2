import asyncio
from google import genai
from app.config import get_settings

async def main():
    settings = get_settings()
    client = genai.Client(api_key=settings.google_api_key)
    # The client method to list models depends on the SDK version, let's try the synchronous one too if async fails
    try:
        models = await client.aio.models.list()
        for m in models:
            print(m.name)
    except Exception as e:
        print("Async error:", e)
        models = client.models.list()
        for m in models:
            print(m.name)

if __name__ == "__main__":
    asyncio.run(main())
