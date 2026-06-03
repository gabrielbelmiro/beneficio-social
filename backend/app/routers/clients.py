from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.logging.logger import get_logger
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.security.dependencies import get_current_user
from app.services.audit_service import create_audit_log
from app.services.phone_formatter import format_brazilian_phone


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

logger = get_logger(__name__)

BENEFIT_INCOME_LIMIT = Decimal("2500.00")


def calculate_eligibility(monthly_income: Decimal) -> bool:
    return monthly_income <= BENEFIT_INCOME_LIMIT


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        formatted_phone = format_brazilian_phone(payload.phone)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    client = Client(
        full_name=payload.full_name,
        email=payload.email,
        phone=formatted_phone,
        cpf=payload.cpf,
        monthly_income=payload.monthly_income,
        benefit_eligible=calculate_eligibility(payload.monthly_income)
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    create_audit_log(
        db=db,
        user=current_user,
        action="CREATE_CLIENT",
        resource_type="CLIENT",
        resource_id=str(client.id),
        status="SUCCESS",
        details=f"Cliente criado. eligible={client.benefit_eligible}"
    )

    logger.info(
        f"Cliente criado com sucesso. client_id={client.id}"
    )

    return client


@router.get("", response_model=list[ClientResponse])
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Client).order_by(Client.id.desc()).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    if payload.full_name is not None:
        client.full_name = payload.full_name

    if payload.email is not None:
        client.email = payload.email

    if payload.phone is not None:
        try:
            client.phone = format_brazilian_phone(payload.phone)
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error)
            )

    if payload.cpf is not None:
        client.cpf = payload.cpf

    if payload.monthly_income is not None:
        client.monthly_income = payload.monthly_income
        client.benefit_eligible = calculate_eligibility(payload.monthly_income)

    db.commit()
    db.refresh(client)

    create_audit_log(
        db=db,
        user=current_user,
        action="UPDATE_CLIENT",
        resource_type="CLIENT",
        resource_id=str(client.id),
        status="SUCCESS",
        details="Cliente atualizado"
    )

    logger.info(
        f"Cliente atualizado com sucesso. client_id={client.id}"
    )

    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    client_id_deleted = client.id

    db.delete(client)
    db.commit()

    create_audit_log(
        db=db,
        user=current_user,
        action="DELETE_CLIENT",
        resource_type="CLIENT",
        resource_id=str(client_id_deleted),
        status="SUCCESS",
        details="Cliente removido"
    )

    logger.info(
        f"Cliente removido com sucesso. client_id={client_id_deleted}"
    )

    return None