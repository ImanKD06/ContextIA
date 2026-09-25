from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
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
    db: Session = Depends(get_db)
):
    query_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY"
    )

    similar_chunks = search_similar_chunks(
        db,
        query_embedding,
        limit=5
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in similar_chunks
    )

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "chunk_id": chunk["id"],
                "document_id": chunk["document_id"],
                "similarity": chunk["similarity"]
            }
            for chunk in similar_chunks
        ]
    }