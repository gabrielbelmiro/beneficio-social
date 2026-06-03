import re

JWT_PATTERN = re.compile(r"eyJ[\w-]+\.[\w-]+\.[\w-]+")


def mask_email(email: str) -> str:
    local, sep, domain = email.partition("@")
    if not sep or len(local) < 2:
        return f"***@{domain}"
    return f"{local[:2]}***@{domain}"


def mask_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 4:
        raise ValueError("Invalid phone number")
    return f"***-***-{digits[-4:]}"


def mask_cpf(cpf: str) -> str:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11:
        raise ValueError("Invalid CPF")
    return f"***.***.***-{digits[-2:]}"


def sanitize_message(message: str) -> str:
    return JWT_PATTERN.sub("[JWT_MASKED]", message)
