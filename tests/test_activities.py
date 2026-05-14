"""
Tests for the activities endpoint (GET /activities)
"""


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities
    
    AAA Pattern:
    - Arrange: client is provided by fixture
    - Act: make GET request to /activities
    - Assert: verify 9 activities are returned
    """
    # Arrange
    expected_activity_count = 9
    expected_activity_names = [
        "Chess Club", "Programming Class", "Gym Class",
        "Basketball Club", "Soccer Team", "Drama Club",
        "Art Club", "Debate Club", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities) == expected_activity_count
    assert list(activities.keys()) == expected_activity_names


def test_activity_has_required_fields(client):
    """
    Test that each activity has all required fields
    
    AAA Pattern:
    - Arrange: define required fields
    - Act: fetch activities and check first one
    - Assert: verify all required fields exist
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    first_activity = activities["Chess Club"]
    
    # Assert
    for field in required_fields:
        assert field in first_activity
    assert isinstance(first_activity["participants"], list)
    assert isinstance(first_activity["max_participants"], int)


def test_participants_format(client):
    """
    Test that participants are returned as a list of emails
    
    AAA Pattern:
    - Arrange: expect participants to be list of strings (emails)
    - Act: fetch an activity with participants
    - Assert: verify participants are list of valid emails
    """
    # Arrange
    # (Chess Club has 2 participants from fixtures)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_participants = activities["Chess Club"]["participants"]
    
    # Assert
    assert isinstance(chess_participants, list)
    assert len(chess_participants) == 2
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants
