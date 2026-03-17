"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_new_participant_success(client, fresh_activities):
    """
    Test successful signup of a new participant.
    
    Arrange: Fresh activities and new email not yet registered.
    Act: Make POST request with new email to signup endpoint
    Assert: Verify status 200, response message, and participant added to list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert f"Signed up {email} for {activity_name}" in result["message"]
    assert email in fresh_activities[activity_name]["participants"]


def test_signup_duplicate_participant_rejected(client, fresh_activities):
    """
    Test that duplicate signup is rejected.
    
    Arrange: Participant already registered for Chess Club.
    Act: Attempt signup with same email
    Assert: Verify status 400 and error detail about duplicate
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club participants
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up for this activity" in result["detail"]


def test_signup_activity_full_rejected(client, fresh_activities, monkeypatch):
    """
    Test that signup is rejected when activity is at max capacity.
    
    Arrange: Set max_participants to 2 for Chess Club (already has 2 participants).
    Act: Attempt signup for a new email
    Assert: Verify status 400 and error about activity being full
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    # Chess Club already has 2 participants and we set max to 2
    fresh_activities[activity_name]["max_participants"] = 2
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "Activity is full" in result["detail"]


def test_signup_nonexistent_activity_rejected(client, fresh_activities):
    """
    Test that signup fails for non-existent activity.
    
    Arrange: Activity name that doesn't exist in the system.
    Act: Attempt signup for non-existent activity
    Assert: Verify status 404 and activity not found error
    """
    # Arrange
    activity_name = "Fictional Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_signup_increases_participant_count(client, fresh_activities):
    """
    Test that signup increases the participant count.
    
    Arrange: Get initial participant count for an activity.
    Act: Sign up a new participant
    Assert: Verify participant count increased by 1
    """
    # Arrange
    activity_name = "Tennis Club"
    initial_count = len(fresh_activities[activity_name]["participants"])
    email = "newplayer@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    new_count = len(fresh_activities[activity_name]["participants"])
    assert new_count == initial_count + 1
