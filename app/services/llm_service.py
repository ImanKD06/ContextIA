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
Eres el asistente de ContextIA, un sistema de consulta de documentos.

Tu tarea es responder a la pregunta del usuario utilizando ÚNICAMENTE
la información contenida en el contexto proporcionado.

REGLAS:

1. Utiliza exclusivamente la información presente en el contexto.

2. No utilices conocimientos externos, información general ni datos
   que no aparezcan en el contexto.

3. No inventes, completes ni supongas información que no esté respaldada
   por el contexto.

4. Puedes utilizar información de varios documentos SOLO si esos
   documentos aparecen en el contexto recuperado y la información
   es relevante para responder a la pregunta.

5. Si la respuesta no aparece en el contexto, responde claramente que
   no encuentras información suficiente en los documentos disponibles.

6. Si el contexto contiene información contradictoria, indícalo
   claramente en lugar de elegir una versión por tu cuenta.

7. Responde de forma clara, directa y concisa.

CONTEXTO RECUPERADO:
{context}

PREGUNTA DEL USUARIO:
{question}

RESPUESTA:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
