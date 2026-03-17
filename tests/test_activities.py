"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Test that GET /activities returns all activities with correct structure.
    
    Arrange: Fresh activities fixture provides clean test data.
    Act: Make a GET request to /activities
    Assert: Verify status 200, all activities present, and structure is correct
    """
    # Arrange & Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    
    # Check we got all activities
    assert len(activities_data) == 9
    assert "Chess Club" in activities_data
    assert "Programming Class" in activities_data
    assert "Art Studio" in activities_data


def test_get_activities_includes_participants(client, fresh_activities):
    """
    Test that activities include participants list in response.
    
    Arrange: Fresh activities fixture with predefined participants.
    Act: Make a GET request to /activities
    Assert: Verify each activity has participants array with correct structure
    """
    # Arrange & Act
    response = client.get("/activities")
    
    # Assert
    activities_data = response.json()
    chess_club = activities_data["Chess Club"]
    
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    assert len(chess_club["participants"]) == 2


def test_get_activities_includes_activity_details(client, fresh_activities):
    """
    Test that activities include all required details.
    
    Arrange: Fresh activities fixture.
    Act: Make a GET request to /activities
    Assert: Verify each activity has description, schedule, and max_participants
    """
    # Arrange & Act
    response = client.get("/activities")
    
    # Assert
    activities_data = response.json()
    programming_class = activities_data["Programming Class"]
    
    assert "description" in programming_class
    assert "schedule" in programming_class
    assert "max_participants" in programming_class
    assert programming_class["max_participants"] == 20
    assert "Learn programming fundamentals" in programming_class["description"]
