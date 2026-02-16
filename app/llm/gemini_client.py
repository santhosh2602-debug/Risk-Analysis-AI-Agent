from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def get_llm():
    return ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.google_api_key,
        temperature=0.1, 
        max_retries=6,
        timeout=None
    )