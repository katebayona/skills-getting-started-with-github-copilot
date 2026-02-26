"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client, reset_activities):
        """
        Arrange: Set up test client with existing participant
        Act: Call DELETE endpoint to unregister student
        Assert: Verify student is removed from participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        initial_participants = 2
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify student is removed from participants
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_participants - 1


    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Call DELETE endpoint for non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Underwater Basket Weaving"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_unregister_non_participant(self, client, reset_activities):
        """
        Arrange: Set up test client with student not in activity
        Act: Try to unregister student who isn't signed up
        Assert: Verify 400 error for non-participant
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notastuent@mergington.edu"  # Not signed up
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]


    def test_signup_then_unregister(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Sign up a student, then unregister them
        Assert: Verify participant count returns to original
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = 2
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert signup worked
        assert signup_response.status_code == 200
        activities_after_signup = client.get("/activities").json()
        assert len(activities_after_signup[activity_name]["participants"]) == initial_count + 1
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert unregister worked
        assert unregister_response.status_code == 200
        activities_after_unregister = client.get("/activities").json()
        assert len(activities_after_unregister[activity_name]["participants"]) == initial_count


    def test_unregister_multiple_participants(self, client, reset_activities):
        """
        Arrange: Set up test client with activity that has multiple participants
        Act: Unregister one participant
        Assert: Verify only that participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        participant1 = "michael@mergington.edu"
        participant2 = "daniel@mergington.edu"
        
        # Act - Remove first participant
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={participant1}"
        )
        
        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert participant1 not in activities[activity_name]["participants"]
        assert participant2 in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1
