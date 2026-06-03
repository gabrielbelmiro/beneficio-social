from pydantic import BaseModel


class DocumentAnalysisResponse(BaseModel):
    document_id: int
    client_id: int
    status: str
    reason: str
    income: str | None
    confidence: float