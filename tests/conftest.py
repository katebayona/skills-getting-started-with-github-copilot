"""Pytest configuration and fixtures for FastAPI tests using AAA pattern"""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Fixture: Provides a TestClient for testing FastAPI app (Arrange phase)"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture: Reset activities to initial state before each test (Arrange phase)"""
    # Save initial state
    initial_state = {
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
        "Basketball Team": {
            "description": "Compete in varsity and intramural basketball leagues",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["james@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debate",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and experiments",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        }
    }
    
    yield
    
    # Restore initial state after test (cleanup)
    activities.clear()
    activities.update(initial_state)


@pytest.fixture
def sample_activity():
    """Fixture: Provides sample activity data (Arrange phase)"""
    return {
        "name": "Chess Club",
        "email": "newstudent@mergington.edu"
    }


@pytest.fixture
def existingactivities_fixture():
    """Fixture: Provides information about existing activities (Arrange phase)"""
    return {
        "existing_activity": "Chess Club",
        "existing_participant": "michael@mergington.edu",
        "nonexistent_activity": "Underwater Basket Weaving"
    }
