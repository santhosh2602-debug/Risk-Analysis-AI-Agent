
from langchain_openai import ChatOpenAI
from app.config import settings

def get_llm():
    return ChatOpenAI(
        model="gpt-4o", 
        api_key=settings.openai_api_key,
        temperature=0.1,
        max_retries=5
    )