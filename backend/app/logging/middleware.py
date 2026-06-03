from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging.context import set_execution_context
from app.logging.logger import get_logger


logger = get_logger(__name__)


class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        incoming_execution_id = request.headers.get("X-Execution-Id")

        execution_id = set_execution_context(
            execution_id=incoming_execution_id
        )

        logger.info(
            f"Request started: {request.method} {request.url.path}"
        )

        try:
            response = await call_next(request)

        except Exception:
            logger.exception(
                f"Unhandled error. method={request.method} "
                f"path={request.url.path}"
            )
            raise

        response.headers["X-Execution-Id"] = execution_id

        logger.info(
            f"Request finished: {request.method} "
            f"{request.url.path} "
            f"status={response.status_code}"
        )

        return response