def test_login_success(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401


def test_auth_me_without_token_returns_403(client):
    response = client.get("/auth/me")

    assert response.status_code == 403


def test_auth_me_with_token_returns_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"