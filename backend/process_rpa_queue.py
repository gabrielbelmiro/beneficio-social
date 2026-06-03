import os
import signal
import time
from datetime import datetime, timezone

from app.db.database import SessionLocal
from app.models.client import Client
from app.models.rpa_queue import RPAQueue
from app.services.rpa_service import run_benefit_registration
from app.logging.logger import get_logger


logger = get_logger(__name__)

POLL_INTERVAL_SECONDS = int(os.getenv("RPA_QUEUE_POLL_INTERVAL_SECONDS", "10"))
running = True


def stop_worker(signum, frame):
    global running
    running = False
    logger.info("Sinal de parada recebido. Encerrando worker com segurança...")


signal.signal(signal.SIGINT, stop_worker)
signal.signal(signal.SIGTERM, stop_worker)


def get_next_pending_job(db):
    return (
        db.query(RPAQueue)
        .filter(RPAQueue.status == "PENDING")
        .order_by(RPAQueue.priority.desc(), RPAQueue.created_at.asc())
        .first()
    )


def process_next_job() -> bool:
    db = SessionLocal()

    try:
        job = get_next_pending_job(db)

        if not job:
            logger.info("Nenhum job pendente na fila RPA.")
            return False

        client = db.query(Client).filter(Client.id == job.client_id).first()

        if not client:
            job.status = "FAILED"
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
            logger.error(f"Job RPA falhou: cliente não encontrado. job_id={job.id}")
            return True

        if not client.benefit_eligible:
            job.status = "FAILED"
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
            logger.error(
                f"Job RPA falhou: cliente não elegível. "
                f"job_id={job.id} client_id={client.id}"
            )
            return True

        job.status = "RUNNING"
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        logger.info(f"Job RPA iniciado. job_id={job.id} client_id={client.id}")

        execution = run_benefit_registration(db=db, client=client)

        job.status = "DONE" if execution.status == "SUCCESS" else "FAILED"
        job.finished_at = datetime.now(timezone.utc)

        db.commit()

        logger.info(
            f"Job RPA finalizado. job_id={job.id} "
            f"client_id={client.id} execution_id={execution.execution_id} "
            f"status={job.status}"
        )

        return True

    except Exception:
        db.rollback()
        logger.exception("Erro inesperado ao processar fila RPA.")
        return True

    finally:
        db.close()


def run_worker_loop():
    logger.info(
        f"Worker RPA contínuo iniciado. "
        f"poll_interval={POLL_INTERVAL_SECONDS}s"
    )

    while running:
        processed = process_next_job()

        if not processed:
            time.sleep(POLL_INTERVAL_SECONDS)

    logger.info("Worker RPA contínuo encerrado.")


if __name__ == "__main__":
    run_worker_loop()