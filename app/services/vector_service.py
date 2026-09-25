from sqlalchemy import text
from sqlalchemy.orm import Session


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    limit: int = 5
):
    query = text("""
        SELECT
            id,
            text,
            document_id,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM chunks
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        query,
        {
            "embedding": str(query_embedding),
            "limit": limit
        }
    )

    return result.mappings().all()