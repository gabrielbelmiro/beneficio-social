from app.services.income_analyzer import classify_income, extract_income


def test_extract_income_from_renda_mensal():
    text = "Nome: João da Silva\nRenda mensal: R$ 1.800,00"
    result = extract_income(text)
    assert str(result) == "1800.00"


def test_classify_approved_income():
    text = "Renda mensal: R$ 1.800,00"
    result = classify_income(text)

    assert result["status"] == "APPROVED"
    assert result["confidence"] == 0.90


def test_classify_rejected_income():
    text = "Salário: R$ 4.500,00"
    result = classify_income(text)

    assert result["status"] == "REJECTED"
    assert result["confidence"] == 0.90


def test_classify_inconclusive_when_income_not_found():
    text = "Documento ilegível sem informação de renda"
    result = classify_income(text)

    assert result["status"] == "INCONCLUSIVE"
    assert result["confidence"] == 0.45