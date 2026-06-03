from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class ManualReview(Base):
    __tablename__ = "manual_reviews"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    reviewed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String, nullable=False, default="PENDING")
    ai_reason = Column(Text, nullable=True)
    manual_reason = Column(Text, nullable=True)
    final_decision = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    document = relationship("Document")
    client = relationship("Client")
    reviewed_by = relationship("User")