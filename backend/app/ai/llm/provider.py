from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_llm() -> ChatOpenAI:
    """
    Returns an OpenAI-compatible chat model client.

    We are using OpenRouter as the provider, but keeping this function generic so the rest of the app does not depend directly on OpenRouter details.
    """

    if not settings.OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Add it to your backend/ .env file."
        )
    
    return ChatOpenAI(
        model = settings.LLM_MODEL,
        api_key= settings.OPENROUTER_API_KEY,
        base_url= settings.OPENROUTER_BASE_URL,
        temperature= settings.LLM_TEMPERATURE,
        max_tokens=1200,

    )