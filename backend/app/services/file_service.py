import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException, status


ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "image/png": "png"
}


UPLOAD_BASE_PATH = Path("uploads")


def save_uploaded_file(file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo inválido. Apenas PDF e PNG são permitidos."
        )

    extension = ALLOWED_MIME_TYPES[file.content_type]

    generated_filename = f"{uuid.uuid4()}.{extension}"

    target_folder = UPLOAD_BASE_PATH / extension

    target_folder.mkdir(parents=True, exist_ok=True)

    target_path = target_folder / generated_filename

    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "original_filename": file.filename,
        "stored_filename": generated_filename,
        "mime_type": file.content_type,
        "file_path": str(target_path)
    }