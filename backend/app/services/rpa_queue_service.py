from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.rpa_queue import RPAQueue


def enqueue_client_for_rpa(db: Session, client: Client) -> RPAQueue:
    if not client.benefit_eligible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente não elegível para entrar na fila RPA"
        )

    existing_job = (
        db.query(RPAQueue)
        .filter(
            RPAQueue.client_id == client.id,
            RPAQueue.status.in_(["PENDING", "RUNNING"])
        )
        .first()
    )

    if existing_job:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cliente já possui execução pendente ou em andamento"
        )

    job = RPAQueue(
        client_id=client.id,
        status="PENDING",
        priority=1
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job