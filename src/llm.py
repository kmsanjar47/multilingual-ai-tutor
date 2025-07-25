from src.config import LLM_PROVIDER, GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    if LLM_PROVIDER != "gemini":
        raise ValueError("Configured only for Gemini for now. Change here if you need others.")
    if not GOOGLE_API_KEY:
        raise ValueError("Set GOOGLE_API_KEY for Gemini")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )
