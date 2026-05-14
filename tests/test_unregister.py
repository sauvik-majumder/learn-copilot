"""
Tests for the unregister endpoint (POST /activities/{activity_name}/unregister)
"""


def test_unregister_success(client):
    """
    Test successful unregister from an activity
    
    AAA Pattern:
    - Arrange: prepare email already in participants
    - Act: make POST request to unregister
    - Assert: verify participant removed and success message returned
    """
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert email in result["message"]
    assert activity in result["message"]
    
    # Verify participant was removed
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered_fails(client):
    """
    Test that unregister fails with 400 error when student not registered
    
    AAA Pattern:
    - Arrange: prepare email not in any activity
    - Act: attempt to unregister
    - Assert: verify 400 error
    """
    # Arrange
    email = "never.registered@mergington.edu"
    activity = "Basketball Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not registered" in result["detail"].lower()


def test_unregister_invalid_activity_fails(client):
    """
    Test that unregister fails with 404 error for non-existent activity
    
    AAA Pattern:
    - Arrange: prepare invalid activity name
    - Act: attempt to unregister from non-existent activity
    - Assert: verify 404 error
    """
    # Arrange
    email = "any@mergington.edu"
    activity = "Fake Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()


def test_unregister_signup_then_unregister(client):
    """
    Test signup flow followed by unregister
    
    AAA Pattern:
    - Arrange: prepare email and activity
    - Act: signup first, then unregister
    - Assert: verify signup succeeded then removal succeeded
    """
    # Arrange
    email = "flow.test@mergington.edu"
    activity = "Debate Club"
    
    # Act - Signup
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert signup
    assert signup_response.status_code == 200
    check1 = client.get("/activities")
    assert email in check1.json()[activity]["participants"]
    
    # Act - Unregister
    unregister_response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert unregister
    assert unregister_response.status_code == 200
    check2 = client.get("/activities")
    assert email not in check2.json()[activity]["participants"]


def test_unregister_multiple_participants(client):
    """
    Test unregister removes only the specified participant
    
    AAA Pattern:
    - Arrange: two participants in same activity
    - Act: unregister one
    - Assert: verify only that one was removed, other remains
    """
    # Arrange
    email1 = "michael@mergington.edu"  # In Chess Club
    email2 = "daniel@mergington.edu"   # In Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email1}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify only email1 was removed, email2 still there
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email1 not in activities[activity]["participants"]
    assert email2 in activities[activity]["participants"]


def test_unregister_cannot_unregister_twice(client):
    """
    Test that unregistering twice fails on second attempt
    
    AAA Pattern:
    - Arrange: participant in activity
    - Act: unregister first time (succeeds), then unregister again
    - Assert: verify second unregister fails with 400 error
    """
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act - First unregister
    response1 = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert first unregister
    assert response1.status_code == 200
    
    # Act - Second unregister (should fail)
    response2 = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert second unregister fails
    assert response2.status_code == 400
    result = response2.json()
    assert "not registered" in result["detail"].lower()
