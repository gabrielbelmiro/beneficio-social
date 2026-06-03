from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.security.dependencies import get_current_user
from app.services.file_service import save_uploaded_file


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/clients/{client_id}/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_document(
    client_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    upload_data = save_uploaded_file(file)

    document = Document(
        client_id=client.id,
        original_filename=upload_data["original_filename"],
        stored_filename=upload_data["stored_filename"],
        mime_type=upload_data["mime_type"],
        file_path=upload_data["file_path"]
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document