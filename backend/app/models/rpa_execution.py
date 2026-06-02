from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class RPAExecution(Base):
    __tablename__ = "rpa_executions"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"))

    execution_id = Column(String, unique=True, nullable=False)

    status = Column(String, nullable=False)

    duration_seconds = Column(Numeric(10, 2), nullable=True)

    error_message = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client")