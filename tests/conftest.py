"""
Pytest configuration and fixtures for FastAPI tests.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making HTTP requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Provides a fresh copy of activities for each test to prevent test pollution.
    Uses monkeypatch to replace the app's activities with a deep copy.
    """
    # Create a deep copy of the original activities
    activities_copy = copy.deepcopy(activities)
    
    # Replace the app's activities with the copy for this test
    monkeypatch.setattr("src.app.activities", activities_copy)
    
    return activities_copy
