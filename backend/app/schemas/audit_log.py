from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    user_email: str | None
    action: str
    resource_type: str
    resource_id: str | None
    status: str
    details: str | None
    execution_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True