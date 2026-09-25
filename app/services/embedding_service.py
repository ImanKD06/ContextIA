import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY no está configurada")

client = genai.Client(api_key=api_key)


def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT"
):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values