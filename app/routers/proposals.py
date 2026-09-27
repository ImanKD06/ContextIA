import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.proposal import ProposalRequest, ProposalResponse
from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_similar_chunks_multi
from app.services.proposal_service import generate_proposal
from app.services.report_service import generate_charts
from app.services.report_generator_service import generate_pdf_report

router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"]
)



def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=ProposalResponse)
def create_proposal(
    proposal: ProposalRequest,
    db: Session = Depends(get_db)
):
    if not proposal.document_ids:
        raise HTTPException(
            status_code=400,
            detail="Debes seleccionar al menos un documento"
        )

    query_embedding = generate_embedding(
        proposal.request,
        task_type="RETRIEVAL_QUERY"
    )

    similar_chunks = search_similar_chunks_multi(
        db=db,
        query_embedding=query_embedding,
        document_ids=proposal.document_ids,
        top_k=8,
        similarity_threshold=0.60
    )
    print("\n===== CHUNKS RECUPERADOS =====")

    for chunk in similar_chunks:
        print("ID:", chunk["id"])
        print("DOCUMENTO:", chunk["document_id"])
        print("TÍTULO:", chunk["title"])
        print("SIMILITUD:", chunk["similarity"])
        print("TEXTO:", chunk["text"])
        print("-----------------------------")

    print("===== FIN CHUNKS =====\n")
    
    if not similar_chunks:
        raise HTTPException(
            status_code=404,
            detail=(
                "No se ha encontrado información suficiente "
                "en los documentos seleccionados."
            )
        )

    context_parts = []

    for chunk in similar_chunks:
        context_parts.append(
            f"""
DOCUMENTO ID: {chunk["document_id"]}
DOCUMENTO: {chunk["title"]}
CHUNK ID: {chunk["id"]}
SIMILITUD: {chunk["similarity"]:.3f}

CONTENIDO:
{chunk["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    print("\n===== CONTEXTO ENVIADO A GEMINI =====")
    print(context)
    print("===== FIN CONTEXTO =====\n")

    result = generate_proposal(
    request=proposal.request,
    context=context
    )
    generated_charts = generate_charts(
        result.get("charts", [])
    )

    result["generated_charts"] = generated_charts
    result["sources"] = [
        {
            "document_id": chunk["document_id"],
            "document_title": chunk["title"],
            "chunk_id": chunk["id"],
            "relevant_content": chunk["text"]
        }
        for chunk in similar_chunks
    ]

    pdf_path = generate_pdf_report(result)

    result["report_url"] = f"/generated_reports/{pdf_path.split(os.sep)[-1]}"

    result["sources"] = [
        {
            "document_id": chunk["document_id"],
            "document_title": chunk["title"],
            "chunk_id": chunk["id"],
            "relevant_content": chunk["text"]
        }
        for chunk in similar_chunks
    ]

    return {
        "request": proposal.request,
        "document_ids": proposal.document_ids,
        **result
    }