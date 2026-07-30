def test_root_redirect(client):
    # Arrange - client fixture provides TestClient and reset_activities ensures fresh state

    # Act
    resp = client.get("/", follow_redirects=False)

    # Assert
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@example.com"

    # Act - signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act - duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert duplicate attempt fails
    assert resp2.status_code == 400


def test_remove_participant_and_missing(client):
    # Arrange
    activity = "Chess Club"
    email = "removeme@example.com"

    # Add participant first
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # Act - remove participant
    resp2 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp2.status_code == 200

    # Act - attempt to remove non-existent participant
    resp3 = client.delete(f"/activities/{activity}/participants", params={"email": "noone@example.com"})
    assert resp3.status_code == 404
