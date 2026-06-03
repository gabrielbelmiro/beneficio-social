from fastapi import FastAPI

from app.core.config import settings
from app.logging.middleware import LoggingContextMiddleware
from app.routers import (
    health,
    auth,
    clients,
    documents
)


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)

app.add_middleware(LoggingContextMiddleware)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(documents.router)


@app.get("/")
def root():
    return {
        "message": "Beneficio Social API",
        "docs": "/docs"
    }