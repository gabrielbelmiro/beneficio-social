from pydantic import BaseModel

class RPAQueueResponse(BaseModel):
    id: int
    client_id: int
    status: str
    priority: int
    error_message: str | None = None
    
    class Config:
        from_attributes = True