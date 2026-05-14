"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)
"""
import pytest


def test_signup_success(client):
    """
    Test successful signup for an activity
    
    AAA Pattern:
    - Arrange: prepare email and activity name
    - Act: make POST request to signup
    - Assert: verify participant added and success message returned
    """
    # Arrange
    email = "new.student@mergington.edu"
    activity = "Basketball Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in result["message"]
    assert activity in result["message"]
    
    # Verify participant was added by fetching activities
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_email_fails(client):
    """
    Test that signup fails with 400 error when student already registered
    
    AAA Pattern:
    - Arrange: use an email already in Chess Club participants
    - Act: attempt to signup for the same activity
    - Assert: verify 400 error and appropriate message
    """
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"].lower()


def test_signup_invalid_activity_fails(client):
    """
    Test that signup fails with 404 error for non-existent activity
    
    AAA Pattern:
    - Arrange: prepare invalid activity name
    - Act: attempt to signup for non-existent activity
    - Assert: verify 404 error
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "Non-Existent Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()


def test_signup_multiple_different_activities(client):
    """
    Test that same student can signup for multiple different activities
    
    AAA Pattern:
    - Arrange: prepare email and two different activities
    - Act: signup for first activity, then second
    - Assert: verify both signups succeed
    """
    # Arrange
    email = "multi.student@mergington.edu"
    activity1 = "Basketball Club"
    activity2 = "Art Club"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both activities contain the student
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]


def test_signup_with_special_characters_in_activity_name(client):
    """
    Test that activity names with spaces are properly encoded in URL
    
    AAA Pattern:
    - Arrange: use activity with spaces in name
    - Act: signup with proper URL encoding
    - Assert: verify signup succeeds
    """
    # Arrange
    email = "special@mergington.edu"
    activity = "Programming Class"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was added
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email in activities[activity]["participants"]


def test_signup_various_email_formats(client):
    """
    Test that various valid email formats are accepted
    
    AAA Pattern:
    - Arrange: prepare different email formats
    - Act: signup with each format
    - Assert: verify all succeed
    """
    # Arrange
    emails = [
        "simple@mergington.edu",
        "with+tag@mergington.edu",
        "with.dot@mergington.edu",
        "mixed_char123@mergington.edu"
    ]
    activity = "Drama Club"
    
    # Act & Assert
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200, f"Failed for email: {email}"
