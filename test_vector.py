from app.database import SessionLocal
from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_similar_chunks


db = SessionLocal()

try:
    question = "¿Qué es ContextIA?"

    embedding = generate_embedding(question)

    results = search_similar_chunks(
        db=db,
        query_embedding=embedding,
        limit=5
    )

    for result in results:
        print(result)

finally:
    db.close()