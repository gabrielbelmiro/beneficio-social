from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    client_id: int
    original_filename: str
    stored_filename: str
    mime_type: str
    file_path: str

    class Config:
        from_attributes = True