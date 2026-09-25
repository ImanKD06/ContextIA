from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate
from app.services.chunking_service import split_text
from app.services.embedding_service import generate_embedding

from app.database import SessionLocal
from app.models.document import Document
from app.models.chunk import Chunk


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.get("")
def get_documents(
    db: Session = Depends(get_db)
):
    documents = db.query(Document).all()

    return [
        {
            "id": document.id,
            "title": document.title,
            "content": document.content
        }
        for document in documents
    ]

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return {
            "message": "Document not found"
        }

    return {
        "id": document.id,
        "title": document.title,
        "content": document.content
    }


@router.post("")
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):

    db_document = Document(
        title=document.title,
        content=document.content
    )

    db.add(db_document)

    db.commit()

    db.refresh(db_document)


    chunks = split_text(document.content)


    for chunk_text in chunks:

        embedding = generate_embedding(chunk_text)

        db_chunk = Chunk(
            text=chunk_text,
            embedding=embedding,
            document_id=db_document.id
        )

        db.add(db_chunk)


    db.commit()


    return {
        "message": "Document saved successfully",
        "document_id": db_document.id,
        "title": db_document.title,
        "chunks_created": len(chunks)
    }

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return {
            "message": "Document not found"
        }

    # Eliminar los chunks asociados
    db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete(synchronize_session=False)

    # Eliminar el documento
    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }