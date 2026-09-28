from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate
from app.services.chunking_service import split_text
from app.services.embedding_service import generate_embedding
from app.services.file_service import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx
)

from app.core.database import SessionLocal
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

    db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete(synchronize_session=False)

    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }

@router.post("/upload")
async def upload_documents(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    uploaded_documents = []
    errors = []

    for file in files:

        filename = file.filename.lower()

        try:

            if filename.endswith(".txt"):
                content = await extract_text_from_txt(file)

            elif filename.endswith(".pdf"):
                content = await extract_text_from_pdf(file)

            elif filename.endswith(".docx"):
                content = await extract_text_from_docx(file)

            else:
                errors.append({
                    "filename": file.filename,
                    "error": "Only .txt, .pdf and .docx files are currently supported"
                })
                continue

            if not content.strip():
                errors.append({
                    "filename": file.filename,
                    "error": "The uploaded document contains no readable text"
                })
                continue

            document = Document(
                title=file.filename,
                content=content
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            chunks = split_text(content)

            for chunk_text in chunks:

                embedding = generate_embedding(
                    chunk_text,
                    task_type="RETRIEVAL_DOCUMENT"
                )

                db_chunk = Chunk(
                    text=chunk_text,
                    embedding=embedding,
                    document_id=document.id
                )

                db.add(db_chunk)

            db.commit()

            uploaded_documents.append({
                "document_id": document.id,
                "filename": file.filename,
                "chunks_created": len(chunks)
            })

        except Exception as e:

            db.rollback()

            errors.append({
                "filename": file.filename,
                "error": str(e)
            })

    return {
        "message": "Documents upload process completed",
        "documents": uploaded_documents,
        "errors": errors
    }
