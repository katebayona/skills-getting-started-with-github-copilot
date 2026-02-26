"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client, reset_activities, sample_activity):
        """
        Arrange: Set up test client and sample activity data
        Act: Call POST endpoint to sign up for Chess Club
        Assert: Verify student is added to participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_participants = 2
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify student is in participants
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_participants + 1


    def test_signup_nonexistent_activity(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Call POST endpoint for non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Underwater Basket Weaving"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_signup_duplicate_participant(self, client, reset_activities):
        """
        Arrange: Set up test client with existing participant
        Act: Try to sign up same student twice
        Assert: Verify 400 error for duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


    def test_signup_multiple_students_different_activities(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Sign up different students for different activities
        Assert: Verify each signup succeeds independently
        """
        # Arrange
        student1_email = "random1@mergington.edu"
        student2_email = "random2@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act - Sign up student 1
        response1 = client.post(
            f"/activities/{activity1}/signup?email={student1_email}"
        )
        
        # Act - Sign up student 2
        response2 = client.post(
            f"/activities/{activity2}/signup?email={student2_email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities = client.get("/activities").json()
        assert student1_email in activities[activity1]["participants"]
        assert student2_email in activities[activity2]["participants"]
        assert student1_email not in activities[activity2]["participants"]
        assert student2_email not in activities[activity1]["participants"]
