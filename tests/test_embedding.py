import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="ContextIA es una aplicación de inteligencia artificial para buscar información en documentos.",
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768
    )
)

embedding = result.embeddings[0].values

print("Dimensión:", len(embedding))
print("Primeros valores:", embedding[:5])