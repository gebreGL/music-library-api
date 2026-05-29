import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_artist():
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/artists",
        json={
            "name": f"Artist {unique_id}",
            "country": "Spain",
            "genre": "Pop",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == f"Artist {unique_id}"
    assert response.json()["country"] == "Spain"
    assert response.json()["genre"] == "Pop"
    assert "id" in response.json()