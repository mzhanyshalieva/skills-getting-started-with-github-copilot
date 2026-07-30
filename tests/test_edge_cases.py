from fastapi import HTTPException


def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "ghost@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_remove_from_nonexistent_activity(client):
    # Arrange
    activity = "No Club"
    email = "nobody@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup")

    # Assert
    assert resp.status_code == 422
