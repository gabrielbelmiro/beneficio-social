from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.models.manual_review import ManualReview
from app.models.user import User
from app.schemas.document_analysis import DocumentAnalysisResponse
from app.security.dependencies import get_current_user
from app.services.ocr_service import extract_text
from app.services.income_analyzer import classify_income
from app.logging.logger import get_logger


router = APIRouter(
    prefix="/document-analysis",
    tags=["Document Analysis"]
)

logger = get_logger(__name__)


@router.post("/{document_id}/analyze", response_model=DocumentAnalysisResponse)
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )

    try:
        extracted_text = extract_text(
            file_path=document.file_path,
            mime_type=document.mime_type
        )

        result = classify_income(extracted_text)

        if result["status"] == "INCONCLUSIVE":
            review = ManualReview(
                document_id=document.id,
                client_id=document.client_id,
                status="PENDING",
                ai_reason=result["reason"]
            )

            db.add(review)
            db.commit()

            logger.info(
                f"Documento enviado para revisão humana. "
                f"document_id={document.id} client_id={document.client_id}"
            )

        logger.info(
            f"Documento analisado. document_id={document.id} "
            f"client_id={document.client_id} status={result['status']} "
            f"confidence={result['confidence']}"
        )

        return DocumentAnalysisResponse(
            document_id=document.id,
            client_id=document.client_id,
            status=result["status"],
            reason=result["reason"],
            income=result["income"],
            confidence=result["confidence"]
        )

    except Exception:
        logger.exception(
            f"Erro ao analisar documento. document_id={document.id}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao analisar documento"
        )