"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


def test_remove_participant_success(client, fresh_activities):
    """
    Test successful removal of a participant.
    
    Arrange: Participant exists in activity.
    Act: Make DELETE request to remove participant
    Assert: Verify status 200, response message, and participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Exists in Chess Club
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert f"Removed {email} from {activity_name}" in result["message"]
    assert email not in fresh_activities[activity_name]["participants"]


def test_remove_nonexistent_participant_rejected(client, fresh_activities):
    """
    Test that removing non-existent participant is rejected.
    
    Arrange: Email not in activity's participants list.
    Act: Attempt DELETE for non-existent participant
    Assert: Verify status 404 and error about participant not found
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notasignup@mergington.edu"  # Not in participants
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found in this activity" in result["detail"]


def test_remove_from_nonexistent_activity_rejected(client, fresh_activities):
    """
    Test that removing participant from non-existent activity is rejected.
    
    Arrange: Activity name that doesn't exist.
    Act: Attempt DELETE from non-existent activity
    Assert: Verify status 404 and error about activity not found
    """
    # Arrange
    activity_name = "Fictional Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_remove_participant_decreases_count(client, fresh_activities):
    """
    Test that removal decreases participant count.
    
    Arrange: Get initial participant count for an activity.
    Act: Remove a participant
    Assert: Verify participant count decreased by 1
    """
    # Arrange
    activity_name = "Music Ensemble"
    initial_count = len(fresh_activities[activity_name]["participants"])
    email = "liam@mergington.edu"  # Exists in Music Ensemble
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    new_count = len(fresh_activities[activity_name]["participants"])
    assert new_count == initial_count - 1


def test_remove_multiple_participants_sequentially(client, fresh_activities):
    """
    Test removing multiple participants in sequence.
    
    Arrange: Activity has multiple participants.
    Act: Remove participants one by one
    Assert: Verify each removal reduces count and removes correct participant
    """
    # Arrange
    activity_name = "Programming Class"
    email1 = "emma@mergington.edu"
    email2 = "sophia@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act - Remove first participant
    response1 = client.delete(
        f"/activities/{activity_name}/participants/{email1}"
    )
    
    # Assert - First removal successful
    assert response1.status_code == 200
    assert email1 not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1
    
    # Act - Remove second participant
    response2 = client.delete(
        f"/activities/{activity_name}/participants/{email2}"
    )
    
    # Assert - Second removal successful
    assert response2.status_code == 200
    assert email2 not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 2
