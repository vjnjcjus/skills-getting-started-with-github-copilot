"""
Tests for the root endpoint (GET /).
"""

import pytest


def test_root_redirects_to_static_index(client):
    """
    Test that the root endpoint redirects to /static/index.html.
    
    Arrange: No setup needed, client is provided by fixture.
    Act: Make a GET request to / with follow_redirects=False
    Assert: Verify redirect status code 307 and location header
    """
    # Arrange & Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
