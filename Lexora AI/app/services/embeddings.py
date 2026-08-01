import os
from dotenv import load_dotenv
from google import genai
from config import Config


def get_client():
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY") or getattr(Config, "GEMINI_API_KEY", None)
    if not api_key or not api_key.strip() or api_key == "your-gemini-api-key-here":
        raise ValueError("Gemini API key is missing. Please open your .env file and add your GEMINI_API_KEY.")
    return genai.Client(api_key=api_key.strip())


def embed_text(text: str):
    client = get_client()
    model_name = getattr(Config, "EMBEDDING_MODEL", "text-embedding-004")
    response = client.models.embed_content(
        model=model_name,
        contents=text,
    )
    return response.embeddings[0].values


def embed_chunks(chunks):
    return [embed_text(chunk) for chunk in chunks]