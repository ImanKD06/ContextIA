from sqlalchemy import text
from sqlalchemy.orm import Session


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    document_id: int,
    top_k: int = 5,
    similarity_threshold: float = 0.60
):
    query = text("""
        SELECT
            chunks.id,
            chunks.text,
            chunks.document_id,
            documents.title,
            1 - (
                chunks.embedding <=> CAST(:embedding AS vector)
            ) AS similarity
        FROM chunks
        JOIN documents
            ON documents.id = chunks.document_id
        WHERE chunks.embedding IS NOT NULL
          AND chunks.document_id = :document_id
          AND 1 - (
              chunks.embedding <=> CAST(:embedding AS vector)
          ) >= :threshold
        ORDER BY chunks.embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        query,
        {
            "embedding": str(query_embedding),
            "document_id": document_id,
            "threshold": similarity_threshold,
            "limit": top_k
        }
    )

    return result.mappings().all()


def search_similar_chunks_multi(
    db: Session,
    query_embedding: list[float],
    document_ids: list[int],
    top_k: int = 8,
    similarity_threshold: float = 0.60
):
    query = text("""
        SELECT
            chunks.id,
            chunks.text,
            chunks.document_id,
            documents.title,
            1 - (
                chunks.embedding <=> CAST(:embedding AS vector)
            ) AS similarity
        FROM chunks
        JOIN documents
            ON documents.id = chunks.document_id
        WHERE chunks.embedding IS NOT NULL
          AND chunks.document_id = ANY(
              CAST(:document_ids AS INTEGER[])
          )
          AND 1 - (
              chunks.embedding <=> CAST(:embedding AS vector)
          ) >= :threshold
        ORDER BY chunks.embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        query,
        {
            "embedding": str(query_embedding),
            "document_ids": "{" + ",".join(
                str(document_id)
                for document_id in document_ids
            ) + "}",
            "threshold": similarity_threshold,
            "limit": top_k
        }
    )

    return result.mappings().all()