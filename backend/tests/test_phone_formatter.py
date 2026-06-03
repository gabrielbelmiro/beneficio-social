import pytest

from app.services.phone_formatter import format_brazilian_phone


def test_format_landline_phone():
    result = format_brazilian_phone("1900000000")
    assert result == "(19) 0000-0000"


def test_format_mobile_phone():
    result = format_brazilian_phone("19900000000")
    assert result == "(19) 90000-0000"


def test_format_phone_with_existing_mask():
    result = format_brazilian_phone("(19) 90000-0000")
    assert result == "(19) 90000-0000"


def test_invalid_phone_raises_error():
    with pytest.raises(ValueError):
        format_brazilian_phone("123")