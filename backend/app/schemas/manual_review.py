from pydantic import BaseModel


class ManualReviewResponse(BaseModel):
    id: int
    document_id: int
    client_id: int
    status: str
    ai_reason: str | None = None
    manual_reason: str | None = None
    final_decision: str | None = None

    class Config:
        from_attributes = True


class ManualReviewDecisionRequest(BaseModel):
    final_decision: str
    manual_reason: str