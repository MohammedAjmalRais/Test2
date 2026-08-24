import asyncio
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.config import get_settings
from dotenv import load_dotenv

load_dotenv()

async def test_groq():
    settings = get_settings()
    print("Testing Groq API with openai/gpt-oss-20b...")
    try:
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name="openai/gpt-oss-20b",
            temperature=0.2
        )
        response = llm.invoke([HumanMessage(content="Hello, are you working?")])
        print("Success! Response:")
        print(response.content)
    except Exception as e:
        print("Error encountered:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test_groq())
