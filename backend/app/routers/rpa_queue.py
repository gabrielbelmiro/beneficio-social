from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.models.rpa_queue import RPAQueue
from app.models.user import User
from app.schemas.rpa_queue import RPAQueueResponse
from app.security.dependencies import get_current_user
from app.services.rpa_queue_service import enqueue_client_for_rpa
from app.logging.logger import get_logger


router = APIRouter(
    prefix="/rpa-queue",
    tags=["RPA Queue"]
)

logger = get_logger(__name__)


@router.post(
    "/clients/{client_id}/enqueue",
    response_model=RPAQueueResponse,
    status_code=status.HTTP_201_CREATED
)
def enqueue_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    job = enqueue_client_for_rpa(db=db, client=client)

    logger.info(
        f"Cliente adicionado à fila RPA. client_id={client.id} job_id={job.id}"
    )

    return job


@router.get("", response_model=list[RPAQueueResponse])
def list_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(RPAQueue)
        .order_by(RPAQueue.created_at.desc())
        .all()
    )


@router.post("/{job_id}/retry", response_model=RPAQueueResponse)
def retry_failed_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(RPAQueue).filter(RPAQueue.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job da fila RPA não encontrado"
        )

    if job.status != "FAILED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas jobs com status FAILED podem ser reprocessados"
        )

    job.status = "PENDING"
    job.error_message = None
    job.started_at = None
    job.finished_at = None

    db.commit()
    db.refresh(job)

    logger.info(
        f"Job RPA reenfileirado para reprocessamento. "
        f"job_id={job.id} client_id={job.client_id}"
    )

    return job