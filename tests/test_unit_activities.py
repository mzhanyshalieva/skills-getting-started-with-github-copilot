import pytest
from fastapi import HTTPException
from src import app as app_module
from src.app import get_activities, signup_for_activity, remove_participant


def test_get_activities_direct():
    # Arrange

    # Act
    result = get_activities()

    # Assert
    assert isinstance(result, dict)
    assert "Chess Club" in result


def test_signup_direct_and_duplicate():
    # Arrange
    activity = "Programming Class"
    email = "unitstudent@example.com"

    # Act - signup
    resp = signup_for_activity(activity, email)

    # Assert
    assert "Signed up" in resp["message"]
    assert email in app_module.activities[activity]["participants"]

    # Act / Assert - duplicate raises HTTPException
    with pytest.raises(HTTPException) as exc:
        signup_for_activity(activity, email)
    assert exc.value.status_code == 400


def test_remove_participant_direct_and_missing():
    # Arrange
    activity = "Programming Class"
    email = "toremove@example.com"

    # Ensure participant exists
    signup_for_activity(activity, email)
    assert email in app_module.activities[activity]["participants"]

    # Act - remove
    resp = remove_participant(activity, email)

    # Assert
    assert "Removed" in resp["message"]

    # Act / Assert - removing non-existent participant raises
    with pytest.raises(HTTPException) as exc2:
        remove_participant(activity, "nobody@example.com")
    assert exc2.value.status_code == 404
