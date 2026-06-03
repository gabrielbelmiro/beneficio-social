from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.models.manual_review import ManualReview
from app.models.user import User
from app.schemas.manual_review import (
    ManualReviewDecisionRequest,
    ManualReviewResponse
)
from app.security.dependencies import get_current_user
from app.logging.logger import get_logger


router = APIRouter(
    prefix="/manual-reviews",
    tags=["Manual Reviews"]
)

logger = get_logger(__name__)


@router.get("", response_model=list[ManualReviewResponse])
def list_pending_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(ManualReview)
        .filter(ManualReview.status == "PENDING")
        .order_by(ManualReview.created_at.desc())
        .all()
    )


@router.post("/{review_id}/decision", response_model=ManualReviewResponse)
def decide_manual_review(
    review_id: int,
    payload: ManualReviewDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.final_decision not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decisão final deve ser APPROVED ou REJECTED"
        )

    review = db.query(ManualReview).filter(ManualReview.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revisão não encontrada"
        )

    if review.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Revisão já foi finalizada"
        )

    client = db.query(Client).filter(Client.id == review.client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    review.status = "DONE"
    review.final_decision = payload.final_decision
    review.manual_reason = payload.manual_reason
    review.reviewed_by_user_id = current_user.id
    review.reviewed_at = datetime.now(timezone.utc)

    client.benefit_eligible = payload.final_decision == "APPROVED"

    db.commit()
    db.refresh(review)

    logger.info(
        f"Revisão humana finalizada. review_id={review.id} "
        f"client_id={client.id} decision={payload.final_decision}"
    )

    return review