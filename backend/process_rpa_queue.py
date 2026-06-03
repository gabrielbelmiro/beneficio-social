from datetime import datetime, timezone

from app.db.database import SessionLocal
from app.models.client import Client
from app.models.rpa_queue import RPAQueue
from app.services.rpa_service import run_benefit_registration
from app.logging.logger import get_logger


logger = get_logger(__name__)


def get_next_pending_job(db):
    return (
        db.query(RPAQueue)
        .filter(RPAQueue.status == "PENDING")
        .order_by(RPAQueue.priority.desc(), RPAQueue.created_at.asc())
        .first()
    )


def process_next_job():
    db = SessionLocal()

    try:
        job = get_next_pending_job(db)

        if not job:
            logger.info("Nenhum job pendente na fila RPA.")
            return

        client = db.query(Client).filter(Client.id == job.client_id).first()

        if not client:
            job.status = "FAILED"
            job.finished_at = datetime.now(timezone.utc)
            db.commit()

            logger.error(
                f"Job RPA falhou: cliente não encontrado. job_id={job.id}"
            )
            return

        if not client.benefit_eligible:
            job.status = "FAILED"
            job.finished_at = datetime.now(timezone.utc)
            db.commit()

            logger.error(
                f"Job RPA falhou: cliente não elegível. "
                f"job_id={job.id} client_id={client.id}"
            )
            return

        job.status = "RUNNING"
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        logger.info(
            f"Job RPA iniciado. job_id={job.id} client_id={client.id}"
        )

        execution = run_benefit_registration(db=db, client=client)

        if execution.status == "SUCCESS":
            job.status = "DONE"
        else:
            job.status = "FAILED"

        job.finished_at = datetime.now(timezone.utc)
        db.commit()

        logger.info(
            f"Job RPA finalizado. job_id={job.id} "
            f"client_id={client.id} execution_id={execution.execution_id} "
            f"status={job.status}"
        )

    except Exception:
        db.rollback()
        logger.exception("Erro inesperado ao processar fila RPA.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    process_next_job()