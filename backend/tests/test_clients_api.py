def test_create_client_success(client, auth_headers):
    response = client.post(
        "/clients",
        headers=auth_headers,
        json={
            "full_name": "João Teste",
            "email": "joao@test.com",
            "phone": "19900000000",
            "cpf": "12345678900",
            "monthly_income": 1800.00
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "João Teste"
    assert data["phone"] == "(19) 90000-0000"
    assert data["benefit_eligible"] is True


def test_create_client_rejected_by_income(client, auth_headers):
    response = client.post(
        "/clients",
        headers=auth_headers,
        json={
            "full_name": "Maria Teste",
            "email": "maria@test.com",
            "phone": "1900000000",
            "cpf": "98765432100",
            "monthly_income": 5000.00
        }
    )

    assert response.status_code == 201
    assert response.json()["benefit_eligible"] is False


def test_list_clients_requires_auth(client):
    response = client.get("/clients")

    assert response.status_code == 403


def test_list_clients_with_auth(client, auth_headers):
    response = client.get("/clients", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)