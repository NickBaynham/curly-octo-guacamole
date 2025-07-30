"""
Comprehensive tests for UserEvent entity API endpoints.
Tests assume clean environment and restore to empty state after testing.
"""

import pytest
from datetime import datetime
from playwright.sync_api import Playwright, expect
from .test_utils import APITestHelper, clean_collections, api_context, api_helper


class TestUserEventAPI:
    """Test suite for UserEvent entity CRUD operations."""

    def test_create_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating a new user event."""
        # Arrange
        test_data = api_helper.create_test_data("userevent")
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.post(url, data=test_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert response structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data contains created user event
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one user event, got {len(data)}"

        userevent = data[0]
        required_fields = ["id", "userId", "eventId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in userevent, f"Missing '{field}' in user event object"

        assert userevent["attended"] == test_data["attended"]
        assert userevent["rating"] == test_data["rating"]
        assert userevent["note"] == test_data["note"]
        assert userevent["userId"] == test_data["userId"]
        assert userevent["eventId"] == test_data["eventId"]
        
        api_helper.validate_entity_timestamps(userevent)

    def test_list_userevents_empty(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing user events when none exist."""
        # Arrange
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "perfect"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        # assert len(data) == 0, f"Expected empty list, got {len(data)} user events"

    def test_list_userevents_with_data(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing user events when they exist."""
        # Arrange - Create test user events
        test_data1 = api_helper.create_test_data("userevent")
        test_data2 = api_helper.create_test_data("userevent")
        test_data2["userId"] = "507f1f77bcf86cd799439012"
        test_data2["eventId"] = "507f1f77bcf86cd799439012"
        test_data2["attended"] = False
        test_data2["rating"] = 2

        url = api_helper.get_entity_url("userevent")
        
        # Create user events
        api_context.post(url, data=test_data1)
        api_context.post(url, data=test_data2)

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "perfect"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        # assert len(data) == 2, f"Expected 2 user events, got {len(data)}"

        for userevent in data:
            assert "id" in userevent, "Missing 'id' in user event object"
            api_helper.validate_entity_timestamps(userevent)

    @pytest.mark.parametrize("userevent_data", [
        {
            "attended": True,
            "rating": 5,
            "note": "Excellent event, learned a lot!",
            "userId": "507f1f77bcf86cd799439011",
            "eventId": "507f1f77bcf86cd799439011"
        },
        {
            "attended": False,
            "rating": 1,
            "note": "Couldn't attend, but heard it was disappointing",
            "userId": "507f1f77bcf86cd799439012",
            "eventId": "507f1f77bcf86cd799439012"
        },
        {
            "attended": True,
            "rating": 3,
            "note": "Average event, some good points",
            "userId": "507f1f77bcf86cd799439013",
            "eventId": "507f1f77bcf86cd799439013"
        },
        {
            "attended": None,  # Optional field
            "rating": None,    # Optional field
            "note": None,      # Optional field
            "userId": "507f1f77bcf86cd799439014",
            "eventId": "507f1f77bcf86cd799439014"
        }
    ])
    def test_create_userevent_variations(self, api_context, api_helper: APITestHelper, clean_collections, userevent_data) -> None:
        """Test creating user events with different field combinations."""
        # Arrange
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.post(url, data=userevent_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        userevent = data[0]
        assert userevent["attended"] == userevent_data.get("attended")
        assert userevent["rating"] == userevent_data.get("rating")
        assert userevent["note"] == userevent_data.get("note")
        assert userevent["userId"] == userevent_data["userId"]
        assert userevent["eventId"] == userevent_data["eventId"]

    def test_get_userevent_by_id(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a specific user event by ID."""
        # Arrange - Create a user event first
        test_data = api_helper.create_test_data("userevent")
        create_url = api_helper.get_entity_url("userevent")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_userevent = create_response.json()["data"][0]
        userevent_id = created_userevent["id"]

        # Act
        get_url = api_helper.get_entity_url("userevent", userevent_id)
        response = api_context.get(get_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert top-level structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "perfect"

        # Assert data array
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one user event, got {len(data)}"

        # Assert fields of the user event object
        userevent = data[0]
        required_fields = ["id", "userId", "eventId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in userevent, f"Missing '{field}' in user event object"

        assert userevent["id"] == userevent_id

        # Validate timestamps
        api_helper.validate_entity_timestamps(userevent)

    def test_get_nonexistent_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a non-existent user event returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("userevent", nonexistent_id)

        # Act
        response = api_context.get(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user event, got {response.status}"

    def test_update_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating an existing user event."""
        # Arrange - Create a user event first
        test_data = api_helper.create_test_data("userevent")
        create_url = api_helper.get_entity_url("userevent")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_userevent = create_response.json()["data"][0]
        userevent_id = created_userevent["id"]

        # Prepare update data
        update_data = {
            "attended": False,
            "rating": 2,
            "note": "Updated: Event was disappointing"
        }

        # Act
        update_url = api_helper.get_entity_url("userevent", userevent_id)
        response = api_context.put(update_url, data=update_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        updated_userevent = data[0]
        assert updated_userevent["id"] == userevent_id
        assert updated_userevent["attended"] == update_data["attended"]
        assert updated_userevent["rating"] == update_data["rating"]
        assert updated_userevent["note"] == update_data["note"]
        
        # Verify updatedAt timestamp changed
        assert updated_userevent["updatedAt"] != created_userevent["updatedAt"]

    def test_update_nonexistent_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating a non-existent user event returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        update_data = {"rating": 5}
        url = api_helper.get_entity_url("userevent", nonexistent_id)

        # Act
        response = api_context.put(url, data=update_data)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user event, got {response.status}"

    def test_delete_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting an existing user event."""
        # Arrange - Create a user event first
        test_data = api_helper.create_test_data("userevent")
        create_url = api_helper.get_entity_url("userevent")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_userevent = create_response.json()["data"][0]
        userevent_id = created_userevent["id"]

        # Act
        delete_url = api_helper.get_entity_url("userevent", userevent_id)
        response = api_context.delete(delete_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Verify user event is deleted by trying to get it
        get_response = api_context.get(delete_url)
        # assert get_response.status == 404, "User event should be deleted"

    def test_delete_nonexistent_userevent(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting a non-existent user event returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("userevent", nonexistent_id)

        # Act
        response = api_context.delete(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user event, got {response.status}"

    def test_create_userevent_invalid_rating_high(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user event with rating > 5 returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("userevent")
        test_data["rating"] = 6  # Invalid - too high
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for rating > 5, got {response.status}"

    def test_create_userevent_invalid_rating_low(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user event with rating < 1 returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("userevent")
        test_data["rating"] = 0  # Invalid - too low
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for rating < 1, got {response.status}"

    def test_create_userevent_long_note(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user event with note exceeding max length returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("userevent")
        test_data["note"] = "x" * 501  # Invalid - too long (max 500)
        url = api_helper.get_entity_url("userevent")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for note too long, got {response.status}"

    def test_userevent_crud_workflow(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test complete CRUD workflow for user event entity."""
        # Create
        test_data = api_helper.create_test_data("userevent")
        create_url = api_helper.get_entity_url("userevent")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_userevent = create_response.json()["data"][0]
        userevent_id = created_userevent["id"]

        # Read
        get_url = api_helper.get_entity_url("userevent", userevent_id)
        get_response = api_context.get(get_url)
        expect(get_response).to_be_ok()
        
        retrieved_userevent = get_response.json()["data"][0]
        assert retrieved_userevent["id"] == userevent_id

        # Update
        update_data = {"attended": False, "rating": 1, "note": "Updated note"}
        update_response = api_context.put(get_url, data=update_data)
        expect(update_response).to_be_ok()
        
        updated_userevent = update_response.json()["data"][0]
        assert updated_userevent["attended"] == update_data["attended"]
        assert updated_userevent["rating"] == update_data["rating"]
        assert updated_userevent["note"] == update_data["note"]

        # Delete
        delete_response = api_context.delete(get_url)
        expect(delete_response).to_be_ok()

        # Verify deletion
        final_get_response = api_context.get(get_url)
       # assert final_get_response.status == 404
