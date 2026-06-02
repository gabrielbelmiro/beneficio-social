from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import SessionLocal


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "status": "ok",
        "service": "Beneficio Social API" # Validar API
    }


@router.get("/db") 
def database_health_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected" # Validar API x DB
        }
    finally:
        db.close()