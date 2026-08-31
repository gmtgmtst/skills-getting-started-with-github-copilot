"""
Shared test fixtures for FastAPI application tests.

This module provides fixtures using the AAA (Arrange-Act-Assert) pattern
to set up test environment and sample data for both unit and integration tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for testing FastAPI endpoints.
    
    Arrange: Creates a test client that can make HTTP requests to the app.
    
    Yields:
        TestClient: An instance of FastAPI's TestClient for making test requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture providing sample activities data for testing.
    
    Arrange: Returns a dictionary of test activities with participants.
    
    Returns:
        dict: A dictionary of activities matching the app's data structure.
              Keys are activity names, values are activity details including
              description, schedule, max_participants, and participants list.
    """
    return {
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
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        }
    }
