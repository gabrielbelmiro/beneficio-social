from app.security.sanitizers.log_sanitizer import (
    mask_email,
    mask_phone,
    mask_cpf,
    sanitize_message
)


def test_mask_email():
    assert mask_email("gabriel@email.com") == "ga***@email.com"


def test_mask_phone():
    assert mask_phone("(19) 99999-0000") == "***-***-0000"


def test_mask_cpf():
    assert mask_cpf("12345678900") == "***.***.***-00"


def test_sanitize_jwt():
    message = "Token: eyJabc.def.ghi"
    result = sanitize_message(message)

    assert "[JWT_MASKED]" in result