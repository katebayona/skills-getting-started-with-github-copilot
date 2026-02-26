"""Tests for GET /activities endpoint using AAA pattern"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Call GET /activities
        Assert: Verify all 9 activities are returned
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities


    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Call GET /activities
        Assert: Verify each activity has required fields
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        # Verify each activity has required fields
        for name, details in activities.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)


    def test_get_activities_includes_participants(self, client, reset_activities):
        """
        Arrange: Set up test client
        Act: Call GET /activities
        Assert: Verify participants are included in response
        """
        # Arrange (implicit via fixtures)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        # Chess Club should have 2 participants
        assert len(activities["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
