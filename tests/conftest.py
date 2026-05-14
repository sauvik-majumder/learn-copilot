"""
Shared pytest fixtures and configuration for API tests.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for making test requests."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test to ensure test isolation."""
    # Store initial state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Play basketball and develop team skills",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": []
        },
        "Soccer Team": {
            "description": "Compete in soccer matches and practice",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in plays and learn theatrical skills",
            "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other art forms",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop speaking and debate skills",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and learn about science",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        }
    }
    
    # Clear existing activities
    activities.clear()
    
    # Restore initial state
    activities.update(initial_activities)
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(initial_activities)
