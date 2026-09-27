from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_similar_chunks
from app.services.llm_service import generate_answer

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("")
def chat(
    question: str,
    document_id: int,
    db: Session = Depends(get_db)
):
    query_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY"
    )

    similar_chunks = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=5,
        similarity_threshold=0.60
    )

    if not similar_chunks:
        return {
            "question": question,
            "document_id": document_id,
            "answer": (
                "No encuentro información suficiente en este "
                "documento para responder a la pregunta."
            ),
            "sources": []
        }

    context_parts = []

    for chunk in similar_chunks:
        context_parts.append(
            f"""
DOCUMENTO: {chunk["title"]}
SIMILITUD: {chunk["similarity"]:.3f}

CONTENIDO:
{chunk["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
    "question": question,
    "document_id": document_id,
    "answer": answer,
    "sources": [
        {
            "chunk_id": chunk["id"],
            "document_id": chunk["document_id"],
            "document_title": chunk["title"],
            "similarity": round(chunk["similarity"], 3)
        }
        for chunk in similar_chunks
    ]
}
