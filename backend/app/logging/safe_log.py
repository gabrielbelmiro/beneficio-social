from app.security.sanitizers.log_sanitizer import (
    mask_email,
    mask_phone,
    mask_cpf
)


def safe_client_log(
    email: str | None = None,
    phone: str | None = None,
    cpf: str | None = None
) -> dict:
    return {
        "email": mask_email(email) if email else None,
        "phone": mask_phone(phone) if phone else None,
        "cpf": mask_cpf(cpf) if cpf else None
    }