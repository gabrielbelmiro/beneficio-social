from pydantic import BaseModel


class RPAQueueResponse(BaseModel):
    id: int
    client_id: int
    status: str
    priority: int

    class Config:
        from_attributes = True