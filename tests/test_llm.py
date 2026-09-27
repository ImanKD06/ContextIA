from app.services.llm_service import generate_answer


context = """
ContextIA es una aplicación que utiliza inteligencia artificial
para buscar información relevante dentro de documentos.
Los documentos se dividen en fragmentos y cada fragmento recibe
un embedding.
"""

question = "¿Qué es ContextIA?"

answer = generate_answer(
    question=question,
    context=context
)

print(answer)