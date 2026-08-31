"""
Integration tests for FastAPI endpoints.

This module tests all API endpoints using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and prerequisites
- Act: Call the endpoint being tested
- Assert: Verify the response and side effects

Tests cover happy path scenarios and error cases.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities with participant details.
        
        Arrange: Client is ready (from fixture)
        Act: Make GET request to /activities
        Assert: Status is 200, response contains activities with expected structure
        """
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        
        # Verify structure of an activity
        for activity_name, activity_details in activities.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_get_activities_includes_participants(self, client):
        """
        Test that GET /activities returns participants for activities.
        
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Response includes activities with participant data
        """
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        # At least one activity should have participants from fixtures
        has_participants = any(
            len(activity["participants"]) > 0 
            for activity in activities.values()
        )
        assert has_participants


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_success(self, client):
        """
        Test successful signup of a new participant for an activity.
        
        Arrange: Prepare email and existing activity name
        Act: Send POST request to signup endpoint
        Assert: Status is 200, participant is added to activity
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity in result["message"]

    def test_signup_duplicate_email_returns_error(self, client):
        """
        Test that signup with duplicate email returns error.
        
        Arrange: Use email already signed up for Chess Club
        Act: Send POST request to signup endpoint with same email
        Assert: Status is 400 or 409, includes error detail
        """
        # Arrange
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={duplicate_email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code in [400, 409]
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signup for nonexistent activity returns 404.
        
        Arrange: Use activity name that doesn't exist
        Act: Send POST request to signup endpoint
        Assert: Status is 404, includes error detail
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_signup_with_url_encoding(self, client):
        """
        Test signup with email that needs URL encoding (contains special chars).
        
        Arrange: Use email with special characters
        Act: Send POST request with URL-encoded email
        Assert: Status is 200, signup successful
        """
        # Arrange
        email = "new+tag@mergington.edu"  # Email with special char
        activity = "Programming Class"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_success(self, client):
        """
        Test successful removal of a participant from an activity.
        
        Arrange: Use email and activity where participant exists
        Act: Send DELETE request to remove participant
        Assert: Status is 200, success message returned
        """
        # Arrange
        email = "michael@mergington.edu"  # Participant in Chess Club
        activity = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity in result["message"]

    def test_remove_nonexistent_participant_returns_404(self, client):
        """
        Test that removing nonexistent participant returns 404.
        
        Arrange: Use email not in any activity
        Act: Send DELETE request
        Assert: Status is 404, includes error detail
        """
        # Arrange
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """
        Test that removing from nonexistent activity returns 404.
        
        Arrange: Use activity name that doesn't exist
        Act: Send DELETE request
        Assert: Status is 404, includes error detail
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Activity"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result


class TestRedirectRoot:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that root endpoint redirects to static/index.html.
        
        Arrange: Client is ready
        Act: Make GET request to /
        Assert: Status is 307 or 308 (redirect)
        """
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code in [307, 308]
        assert "/static" in response.headers.get("location", "")
