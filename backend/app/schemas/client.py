from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field


class ClientBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    phone: str
    cpf: str | None = None
    monthly_income: Decimal = Field(..., ge=0)


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    cpf: str | None = None
    monthly_income: Decimal | None = Field(default=None, ge=0)


class ClientResponse(ClientBase):
    id: int
    benefit_eligible: bool

    class Config:
        from_attributes = True