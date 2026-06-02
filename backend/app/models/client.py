from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    cpf = Column(String, nullable=True)

    monthly_income = Column(Numeric(10, 2), nullable=False)

    benefit_eligible = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())