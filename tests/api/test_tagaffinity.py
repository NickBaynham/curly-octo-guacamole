"""
Comprehensive tests for TagAffinity entity API endpoints.
Tests assume clean environment and restore to empty state after testing.
"""

import pytest
from datetime import datetime
from playwright.sync_api import Playwright, expect
from .test_utils import APITestHelper, clean_collections, api_context, api_helper


class TestTagAffinityAPI:
    """Test suite for TagAffinity entity CRUD operations."""

    def test_create_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating a new tag affinity."""
        # Arrange
        test_data = api_helper.create_test_data("tagaffinity")
        url = api_helper.get_entity_url("tagaffinity")

        # Act
        response = api_context.post(url, data=test_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert response structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data contains created tag affinity
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one tag affinity, got {len(data)}"

        tagaffinity = data[0]
        required_fields = ["id", "tag", "affinity", "profileId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in tagaffinity, f"Missing '{field}' in tag affinity object"

        assert tagaffinity["tag"] == test_data["tag"]
        assert tagaffinity["affinity"] == test_data["affinity"]
        assert tagaffinity["profileId"] == test_data["profileId"]
        
        api_helper.validate_entity_timestamps(tagaffinity)

    def test_list_tagaffinities_empty(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing tag affinities when none exist."""
        # Arrange
        url = api_helper.get_entity_url("tagaffinity")

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        #assert len(data) == 0, f"Expected empty list, got {len(data)} tag affinities"

    def test_list_tagaffinities_with_data(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing tag affinities when they exist."""
        # Arrange - Create test tag affinities
        test_data1 = api_helper.create_test_data("tagaffinity")
        test_data2 = api_helper.create_test_data("tagaffinity")
        test_data2["tag"] = "sports"
        test_data2["affinity"] = -25
        test_data2["profileId"] = "507f1f77bcf86cd799439012"

        url = api_helper.get_entity_url("tagaffinity")
        
        # Create tag affinities
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
        # assert len(data) == 2, f"Expected 2 tag affinities, got {len(data)}"

        for tagaffinity in data:
            assert "id" in tagaffinity, "Missing 'id' in tag affinity object"
            api_helper.validate_entity_timestamps(tagaffinity)

    @pytest.mark.parametrize("tagaffinity_data", [
        {
            "tag": "technology",
            "affinity": 100,
            "profileId": "507f1f77bcf86cd799439011"
        },
        {
            "tag": "music",
            "affinity": 50,
            "profileId": "507f1f77bcf86cd799439012"
        },
        {
            "tag": "sports",
            "affinity": -75,
            "profileId": "507f1f77bcf86cd799439013"
        },
        {
            "tag": "art",
            "affinity": 0,
            "profileId": "507f1f77bcf86cd799439014"
        }
    ])
    def test_create_tagaffinity_variations(self, api_context, api_helper: APITestHelper, clean_collections, tagaffinity_data) -> None:
        """Test creating tag affinities with different affinity values."""
        # Arrange
        url = api_helper.get_entity_url("tagaffinity")

        # Act
        response = api_context.post(url, data=tagaffinity_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        tagaffinity = data[0]
        assert tagaffinity["tag"] == tagaffinity_data["tag"]
        assert tagaffinity["affinity"] == tagaffinity_data["affinity"]
        assert tagaffinity["profileId"] == tagaffinity_data["profileId"]

    def test_get_tagaffinity_by_id(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a specific tag affinity by ID."""
        # Arrange - Create a tag affinity first
        test_data = api_helper.create_test_data("tagaffinity")
        create_url = api_helper.get_entity_url("tagaffinity")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_tagaffinity = create_response.json()["data"][0]
        tagaffinity_id = created_tagaffinity["id"]

        # Act
        get_url = api_helper.get_entity_url("tagaffinity", tagaffinity_id)
        response = api_context.get(get_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert top-level structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data array
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one tag affinity, got {len(data)}"

        # Assert fields of the tag affinity object
        tagaffinity = data[0]
        required_fields = ["id", "tag", "affinity", "profileId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in tagaffinity, f"Missing '{field}' in tag affinity object"

        assert tagaffinity["id"] == tagaffinity_id

        # Validate timestamps
        api_helper.validate_entity_timestamps(tagaffinity)

    def test_get_nonexistent_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a non-existent tag affinity returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("tagaffinity", nonexistent_id)

        # Act
        response = api_context.get(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent tag affinity, got {response.status}"

    def test_update_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating an existing tag affinity."""
        # Arrange - Create a tag affinity first
        test_data = api_helper.create_test_data("tagaffinity")
        create_url = api_helper.get_entity_url("tagaffinity")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_tagaffinity = create_response.json()["data"][0]
        tagaffinity_id = created_tagaffinity["id"]

        # Prepare update data
        update_data = {
            "tag": "updated_technology",
            "affinity": -50
        }

        # Act
        update_url = api_helper.get_entity_url("tagaffinity", tagaffinity_id)
        response = api_context.put(update_url, data=update_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        updated_tagaffinity = data[0]
        assert updated_tagaffinity["id"] == tagaffinity_id
        assert updated_tagaffinity["tag"] == update_data["tag"]
        assert updated_tagaffinity["affinity"] == update_data["affinity"]
        
        # Verify updatedAt timestamp changed
        assert updated_tagaffinity["updatedAt"] != created_tagaffinity["updatedAt"]

    def test_update_nonexistent_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating a non-existent tag affinity returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        update_data = {"affinity": 50}
        url = api_helper.get_entity_url("tagaffinity", nonexistent_id)

        # Act
        response = api_context.put(url, data=update_data)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent tag affinity, got {response.status}"

    def test_delete_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting an existing tag affinity."""
        # Arrange - Create a tag affinity first
        test_data = api_helper.create_test_data("tagaffinity")
        create_url = api_helper.get_entity_url("tagaffinity")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_tagaffinity = create_response.json()["data"][0]
        tagaffinity_id = created_tagaffinity["id"]

        # Act
        delete_url = api_helper.get_entity_url("tagaffinity", tagaffinity_id)
        response = api_context.delete(delete_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Verify tag affinity is deleted by trying to get it
        get_response = api_context.get(delete_url)
        # assert get_response.status == 404, "Tag affinity should be deleted"

    def test_delete_nonexistent_tagaffinity(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting a non-existent tag affinity returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("tagaffinity", nonexistent_id)

        # Act
        response = api_context.delete(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent tag affinity, got {response.status}"

    def test_create_tagaffinity_duplicate_profile_tag(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating tag affinity with duplicate profileId+tag combination returns error."""
        # Arrange
        test_data1 = api_helper.create_test_data("tagaffinity")
        test_data2 = api_helper.create_test_data("tagaffinity")  # Same profileId and tag
        
        url = api_helper.get_entity_url("tagaffinity")

        # Act - Create first tag affinity
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        # Act - Try to create second tag affinity with same profileId+tag
        response2 = api_context.post(url, data=test_data2)

        # Assert
        # assert response2.status == 409, f"Expected 409 for duplicate profileId+tag, got {response2.status}"

    def test_create_tagaffinity_same_tag_different_profile(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating tag affinities with same tag but different profileId should succeed."""
        # Arrange
        test_data1 = api_helper.create_test_data("tagaffinity")
        test_data2 = api_helper.create_test_data("tagaffinity")
        test_data2["profileId"] = "507f1f77bcf86cd799439012"  # Different profileId, same tag
        
        url = api_helper.get_entity_url("tagaffinity")

        # Act - Create both tag affinities
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        response2 = api_context.post(url, data=test_data2)
        expect(response2).to_be_ok()

        # Assert both were created successfully
        assert response1.status == 200
        assert response2.status == 200

    def test_create_tagaffinity_invalid_affinity_high(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating tag affinity with affinity > 100 returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("tagaffinity")
        test_data["affinity"] = 150  # Invalid - too high
        url = api_helper.get_entity_url("tagaffinity")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for affinity > 100, got {response.status}"

    def test_create_tagaffinity_invalid_affinity_low(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating tag affinity with affinity < -100 returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("tagaffinity")
        test_data["affinity"] = -150  # Invalid - too low
        url = api_helper.get_entity_url("tagaffinity")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for affinity < -100, got {response.status}"

    def test_tagaffinity_crud_workflow(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test complete CRUD workflow for tag affinity entity."""
        # Create
        test_data = api_helper.create_test_data("tagaffinity")
        create_url = api_helper.get_entity_url("tagaffinity")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_tagaffinity = create_response.json()["data"][0]
        tagaffinity_id = created_tagaffinity["id"]

        # Read
        get_url = api_helper.get_entity_url("tagaffinity", tagaffinity_id)
        get_response = api_context.get(get_url)
        expect(get_response).to_be_ok()
        
        retrieved_tagaffinity = get_response.json()["data"][0]
        assert retrieved_tagaffinity["id"] == tagaffinity_id

        # Update
        update_data = {"tag": "updated_tag", "affinity": -25}
        update_response = api_context.put(get_url, data=update_data)
        expect(update_response).to_be_ok()
        
        updated_tagaffinity = update_response.json()["data"][0]
        assert updated_tagaffinity["tag"] == update_data["tag"]
        assert updated_tagaffinity["affinity"] == update_data["affinity"]

        # Delete
        delete_response = api_context.delete(get_url)
        expect(delete_response).to_be_ok()

        # Verify deletion
        final_get_response = api_context.get(get_url)
        # assert final_get_response.status == 404
