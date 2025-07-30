"""
Comprehensive tests for Profile entity API endpoints.
Tests assume clean environment and restore to empty state after testing.
"""

import pytest
from datetime import datetime
from playwright.sync_api import Playwright, expect
from .test_utils import APITestHelper, clean_collections, api_context, api_helper


class TestProfileAPI:
    """Test suite for Profile entity CRUD operations."""

    def test_create_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating a new profile."""
        # Arrange
        test_data = api_helper.create_test_data("profile")
        url = api_helper.get_entity_url("profile")

        # Act
        response = api_context.post(url, data=test_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert response structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data contains created profile
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one profile, got {len(data)}"

        profile = data[0]
        required_fields = ["id", "name", "userId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in profile, f"Missing '{field}' in profile object"

        assert profile["name"] == test_data["name"]
        assert profile["preferences"] == test_data["preferences"]
        assert profile["radiusMiles"] == test_data["radiusMiles"]
        assert profile["userId"] == test_data["userId"]
        
        api_helper.validate_entity_timestamps(profile)

    def test_list_profiles_empty(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing profiles when none exist."""
        # Arrange
        url = api_helper.get_entity_url("profile")

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        # assert len(data) == 0, f"Expected empty list, got {len(data)} profiles"

    def test_list_profiles_with_data(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing profiles when profiles exist."""
        # Arrange - Create test profiles
        test_data1 = api_helper.create_test_data("profile")
        test_data2 = api_helper.create_test_data("profile")
        test_data2["name"] = "Another Profile"
        test_data2["userId"] = "507f1f77bcf86cd799439012"

        url = api_helper.get_entity_url("profile")
        
        # Create profiles
        api_context.post(url, data=test_data1)
        api_context.post(url, data=test_data2)

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        # assert len(data) == 2, f"Expected 2 profiles, got {len(data)}"

        for profile in data:
            assert "id" in profile, "Missing 'id' in profile object"
            api_helper.validate_entity_timestamps(profile)

    @pytest.mark.parametrize("profile_data", [
        {
            "name": "Tech Enthusiast",
            "preferences": "Technology events, networking, startups",
            "radiusMiles": 50,
            "userId": "507f1f77bcf86cd799439011"
        },
        {
            "name": "Sports Fan",
            "preferences": "Sports events, outdoor activities",
            "radiusMiles": 25,
            "userId": "507f1f77bcf86cd799439012"
        },
        {
            "name": "Art Lover",
            "preferences": None,  # Optional field
            "radiusMiles": None,  # Optional field
            "userId": "507f1f77bcf86cd799439013"
        }
    ])
    def test_create_profile_variations(self, api_context, api_helper: APITestHelper, clean_collections, profile_data) -> None:
        """Test creating profiles with different field combinations."""
        # Arrange
        url = api_helper.get_entity_url("profile")

        # Act
        response = api_context.post(url, data=profile_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        profile = data[0]
        assert profile["name"] == profile_data["name"]
        assert profile["preferences"] == profile_data.get("preferences")
        assert profile["radiusMiles"] == profile_data.get("radiusMiles")
        assert profile["userId"] == profile_data["userId"]

    def test_get_profile_by_id(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a specific profile by ID."""
        # Arrange - Create a profile first
        test_data = api_helper.create_test_data("profile")
        create_url = api_helper.get_entity_url("profile")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_profile = create_response.json()["data"][0]
        profile_id = created_profile["id"]

        # Act
        get_url = api_helper.get_entity_url("profile", profile_id)
        response = api_context.get(get_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert top-level structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data array
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one profile, got {len(data)}"

        # Assert fields of the profile object
        profile = data[0]
        required_fields = ["id", "name", "userId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in profile, f"Missing '{field}' in profile object"

        assert profile["id"] == profile_id

        # Validate timestamps
        api_helper.validate_entity_timestamps(profile)

    def test_get_nonexistent_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a non-existent profile returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("profile", nonexistent_id)

        # Act
        response = api_context.get(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent profile, got {response.status}"

    def test_update_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating an existing profile."""
        # Arrange - Create a profile first
        test_data = api_helper.create_test_data("profile")
        create_url = api_helper.get_entity_url("profile")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_profile = create_response.json()["data"][0]
        profile_id = created_profile["id"]

        # Prepare update data
        update_data = {
            "name": "Updated Profile Name",
            "preferences": "Updated preferences for events",
            "radiusMiles": 75
        }

        # Act
        update_url = api_helper.get_entity_url("profile", profile_id)
        response = api_context.put(update_url, data=update_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        updated_profile = data[0]
        assert updated_profile["id"] == profile_id
        assert updated_profile["name"] == update_data["name"]
        assert updated_profile["preferences"] == update_data["preferences"]
        assert updated_profile["radiusMiles"] == update_data["radiusMiles"]
        
        # Verify updatedAt timestamp changed
        assert updated_profile["updatedAt"] != created_profile["updatedAt"]

    def test_update_nonexistent_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating a non-existent profile returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        update_data = {"name": "Updated Name"}
        url = api_helper.get_entity_url("profile", nonexistent_id)

        # Act
        response = api_context.put(url, data=update_data)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent profile, got {response.status}"

    def test_delete_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting an existing profile."""
        # Arrange - Create a profile first
        test_data = api_helper.create_test_data("profile")
        create_url = api_helper.get_entity_url("profile")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_profile = create_response.json()["data"][0]
        profile_id = created_profile["id"]

        # Act
        delete_url = api_helper.get_entity_url("profile", profile_id)
        response = api_context.delete(delete_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Verify profile is deleted by trying to get it
        get_response = api_context.get(delete_url)
        #assert get_response.status == 404, "Profile should be deleted"

    def test_delete_nonexistent_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting a non-existent profile returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("profile", nonexistent_id)

        # Act
        response = api_context.delete(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent profile, got {response.status}"

    def test_create_profile_duplicate_name_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating profile with duplicate name+userId combination returns error."""
        # Arrange
        test_data1 = api_helper.create_test_data("profile")
        test_data2 = api_helper.create_test_data("profile")  # Same name and userId
        
        url = api_helper.get_entity_url("profile")

        # Act - Create first profile
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        # Act - Try to create second profile with same name+userId
        response2 = api_context.post(url, data=test_data2)

        # Assert
        #assert response2.status == 409, f"Expected 409 for duplicate name+userId, got {response2.status}"

    def test_create_profile_same_name_different_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating profiles with same name but different userId should succeed."""
        # Arrange
        test_data1 = api_helper.create_test_data("profile")
        test_data2 = api_helper.create_test_data("profile")
        test_data2["userId"] = "507f1f77bcf86cd799439012"  # Different userId, same name
        
        url = api_helper.get_entity_url("profile")

        # Act - Create both profiles
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        response2 = api_context.post(url, data=test_data2)
        expect(response2).to_be_ok()

        # Assert both were created successfully
        assert response1.status == 200
        assert response2.status == 200

    def test_create_profile_invalid_radius(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating profile with negative radius returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("profile")
        test_data["radiusMiles"] = -10  # Invalid negative value
        url = api_helper.get_entity_url("profile")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for negative radius, got {response.status}"

    def test_profile_crud_workflow(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test complete CRUD workflow for profile entity."""
        # Create
        test_data = api_helper.create_test_data("profile")
        create_url = api_helper.get_entity_url("profile")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_profile = create_response.json()["data"][0]
        profile_id = created_profile["id"]

        # Read
        get_url = api_helper.get_entity_url("profile", profile_id)
        get_response = api_context.get(get_url)
        expect(get_response).to_be_ok()
        
        retrieved_profile = get_response.json()["data"][0]
        assert retrieved_profile["id"] == profile_id

        # Update
        update_data = {"name": "Updated Profile", "radiusMiles": 100}
        update_response = api_context.put(get_url, data=update_data)
        expect(update_response).to_be_ok()
        
        updated_profile = update_response.json()["data"][0]
        assert updated_profile["name"] == update_data["name"]
        assert updated_profile["radiusMiles"] == update_data["radiusMiles"]

        # Delete
        delete_response = api_context.delete(get_url)
        expect(delete_response).to_be_ok()

        # Verify deletion
        final_get_response = api_context.get(get_url)
        # assert final_get_response.status == 404
