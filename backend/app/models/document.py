from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"))

    original_filename = Column(String, nullable=False)

    stored_filename = Column(String, nullable=False)

    mime_type = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client")