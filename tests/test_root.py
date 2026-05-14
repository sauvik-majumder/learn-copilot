"""
Tests for the root endpoint (GET /)
"""


def test_root_redirects_to_index(client):
    """
    Test that GET / redirects to /static/index.html
    
    AAA Pattern:
    - Arrange: client is provided by fixture
    - Act: make GET request to /
    - Assert: verify redirect status and location
    """
    # Arrange
    # (client fixture already provides the TestClient)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
