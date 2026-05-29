import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_playlist_without_token():
    response = client.post(
        "/playlists",
        json={
            "name": "Unauthorized Playlist",
            "description": "Should fail"
        }
    )

    assert response.status_code == 401


def test_create_playlist_with_token():
    unique_id = uuid.uuid4().hex[:8]

    username = f"user_{unique_id}"
    email = f"{username}@example.com"
    password = "123456"

    # Register user

    client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    # Login

    login_response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )

    token = login_response.json()["access_token"]

    # Create playlist

    playlist_response = client.post(
        "/playlists",
        json={
            "name": "My Playlist",
            "description": "Testing JWT"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert playlist_response.status_code == 200

    data = playlist_response.json()

    assert data["name"] == "My Playlist"
    assert data["description"] == "Testing JWT"
    assert "owner_id" in data