import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY no está configurada")


client = genai.Client(api_key=api_key)


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Eres el asistente de ContextIA.

Responde a la pregunta del usuario utilizando únicamente la información
proporcionada en el contexto.

Si la respuesta no aparece en el contexto, indica claramente que no
encuentras esa información en los documentos disponibles.

No inventes información.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text