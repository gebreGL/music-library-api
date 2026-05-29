import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user():
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/register",
        json={
            "username": f"testuser_{unique_id}",
            "email": f"testuser_{unique_id}@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == f"testuser_{unique_id}"
    assert response.json()["email"] == f"testuser_{unique_id}@example.com"
    assert "password" not in response.json()


def test_login_user():
    unique_id = uuid.uuid4().hex[:8]
    username = f"loginuser_{unique_id}"
    email = f"loginuser_{unique_id}@example.com"
    password = "123456"

    client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"