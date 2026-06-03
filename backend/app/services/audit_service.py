from sqlalchemy.orm import Session

from app.logging.context import get_execution_id
from app.models.audit_log import AuditLog
from app.models.user import User


def create_audit_log(
    db: Session,
    user: User | None,
    action: str,
    resource_type: str,
    resource_id: str | None,
    status: str,
    details: str | None = None
) -> AuditLog:
    audit = AuditLog(
        user_id=user.id if user else None,
        user_email=user.email if user else None,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        status=status,
        details=details,
        execution_id=get_execution_id()
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit