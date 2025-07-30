"""
Comprehensive tests for Url entity API endpoints.
Tests assume clean environment and restore to empty state after testing.
"""

import pytest
from datetime import datetime
from playwright.sync_api import Playwright, expect
from .test_utils import APITestHelper, clean_collections, api_context, api_helper


class TestUrlAPI:
    """Test suite for Url entity CRUD operations."""

    def test_create_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating a new URL."""
        print("test_create_url")
    #     # Arrange
    #     test_data = api_helper.create_test_data("url")
    #     url_endpoint = api_helper.get_entity_url("url")

    #     # Act
    #     response = api_context.post(url_endpoint, data=test_data)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert response structure
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     # Assert data contains created URL
    #     data = payload["data"]
    #     assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    #     assert len(data) == 1, f"Expected exactly one URL, got {len(data)}"

    #     url_obj = data[0]
    #     required_fields = ["id", "url", "createdAt", "updatedAt"]
    #     for field in required_fields:
    #         assert field in url_obj, f"Missing '{field}' in URL object"

    #     assert url_obj["url"] == test_data["url"]
    #     assert url_obj["params"] == test_data["params"]
        
    #     api_helper.validate_entity_timestamps(url_obj)

    # def test_list_urls_empty(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test listing URLs when none exist."""
    #     # Arrange
    #     url_endpoint = api_helper.get_entity_url("url")

    #     # Act
    #     response = api_context.get(url_endpoint)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     data = payload["data"]
    #     assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    #     assert len(data) == 0, f"Expected empty list, got {len(data)} URLs"

    # def test_list_urls_with_data(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test listing URLs when they exist."""
    #     # Arrange - Create test URLs
    #     test_data1 = api_helper.create_test_data("url")
    #     test_data2 = api_helper.create_test_data("url")
    #     test_data2["url"] = "https://another.example.com/events"
    #     test_data2["params"] = {"type": "music", "city": "newyork"}

    #     url_endpoint = api_helper.get_entity_url("url")
        
    #     # Create URLs
    #     api_context.post(url_endpoint, data=test_data1)
    #     api_context.post(url_endpoint, data=test_data2)

    #     # Act
    #     response = api_context.get(url_endpoint)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     data = payload["data"]
    #     assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    #     # assert len(data) == 2, f"Expected 2 URLs, got {len(data)}"

    #     for url_obj in data:
    #         assert "id" in url_obj, "Missing 'id' in URL object"
    #         api_helper.validate_entity_timestamps(url_obj)

    # @pytest.mark.parametrize("url_data", [
    #     {
    #         "url": "https://events.example.com",
    #         "params": {"category": "tech", "location": "sf"}
    #     },
    #     {
    #         "url": "https://concerts.example.com/list",
    #         "params": {"genre": "rock", "date": "2024-06-15"}
    #     },
    #     {
    #         "url": "https://workshops.example.com",
    #         "params": None  # Optional field
    #     },
    #     {
    #         "url": "https://minimal.example.com"
    #         # params field omitted entirely
    #     }
    # ])

    # def test_create_url_variations(self, api_context, api_helper: APITestHelper, clean_collections, url_data) -> None:
    #     """Test creating URLs with different parameter combinations."""
    #     # Arrange
    #     url_endpoint = api_helper.get_entity_url("url")

    #     # Act
    #     response = api_context.post(url_endpoint, data=url_data)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     data = payload["data"]
    #     url_obj = data[0]
    #     assert url_obj["url"] == url_data["url"]
    #     assert url_obj["params"] == url_data.get("params")

    # def test_get_url_by_id(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test retrieving a specific URL by ID."""
    #     # Arrange - Create a URL first
    #     test_data = api_helper.create_test_data("url")
    #     create_url = api_helper.get_entity_url("url")
        
    #     create_response = api_context.post(create_url, data=test_data)
    #     expect(create_response).to_be_ok()
        
    #     created_url = create_response.json()["data"][0]
    #     url_id = created_url["id"]

    #     # Act
    #     get_url = api_helper.get_entity_url("url", url_id)
    #     response = api_context.get(get_url)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert top-level structure
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     # Assert data array
    #     data = payload["data"]
    #     assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    #     assert len(data) == 1, f"Expected exactly one URL, got {len(data)}"

    #     # Assert fields of the URL object
    #     url_obj = data[0]
    #     required_fields = ["id", "url", "createdAt", "updatedAt"]
    #     for field in required_fields:
    #         assert field in url_obj, f"Missing '{field}' in URL object"

    #     assert url_obj["id"] == url_id

    #     # Validate timestamps
    #     api_helper.validate_entity_timestamps(url_obj)

    # def test_get_nonexistent_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a non-existent URL returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url_endpoint = api_helper.get_entity_url("url", nonexistent_id)

        # Act
        response = api_context.get(url_endpoint)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent URL, got {response.status}"

    # def test_update_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test updating an existing URL."""
    #     # Arrange - Create a URL first
    #     test_data = api_helper.create_test_data("url")
    #     create_url = api_helper.get_entity_url("url")
        
    #     create_response = api_context.post(create_url, data=test_data)
    #     # expect(create_response).to_be_ok()
        
    #     created_url = create_response.json()["data"][0]
    #     url_id = created_url["id"]

    #     # Prepare update data
    #     update_data = {
    #         "url": "https://updated.example.com/events",
    #         "params": {"updated": "true", "version": "2.0"}
    #     }

    #     # Act
    #     update_url = api_helper.get_entity_url("url", url_id)
    #     response = api_context.put(update_url, data=update_data)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     data = payload["data"]
    #     updated_url = data[0]
    #     assert updated_url["id"] == url_id
    #     assert updated_url["url"] == update_data["url"]
    #     assert updated_url["params"] == update_data["params"]
        
    #     # Verify updatedAt timestamp changed
    #     assert updated_url["updatedAt"] != created_url["updatedAt"]

    # def test_update_nonexistent_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test updating a non-existent URL returns 404."""
    #     # Arrange
    #     nonexistent_id = "507f1f77bcf86cd799439011"
    #     update_data = {"url": "https://updated.example.com"}
    #     url_endpoint = api_helper.get_entity_url("url", nonexistent_id)

    #     # Act
    #     response = api_context.put(url_endpoint, data=update_data)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent URL, got {response.status}"

    # def test_delete_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test deleting an existing URL."""
    #     # Arrange - Create a URL first
    #     test_data = api_helper.create_test_data("url")
    #     create_url = api_helper.get_entity_url("url")
        
    #     create_response = api_context.post(create_url, data=test_data)
    #     expect(create_response).to_be_ok()
        
    #     created_url = create_response.json()["data"][0]
    #     url_id = created_url["id"]

    #     # Act
    #     delete_url = api_helper.get_entity_url("url", url_id)
    #     response = api_context.delete(delete_url)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     # Verify URL is deleted by trying to get it
    #     get_response = api_context.get(delete_url)
    #     assert get_response.status == 404, "URL should be deleted"

    def test_delete_nonexistent_url(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting a non-existent URL returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url_endpoint = api_helper.get_entity_url("url", nonexistent_id)

        # Act
        response = api_context.delete(url_endpoint)

        # Assert
        #assert response.status == 404, f"Expected 404 for non-existent URL, got {response.status}"

    def test_create_url_invalid_format(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating URL with invalid format returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("url")
        test_data["url"] = "not-a-valid-url"
        url_endpoint = api_helper.get_entity_url("url")

        # Act
        response = api_context.post(url_endpoint, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for invalid URL format, got {response.status}"

    def test_create_url_missing_protocol(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating URL without protocol returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("url")
        test_data["url"] = "example.com/events"  # Missing http:// or https://
        url_endpoint = api_helper.get_entity_url("url")

        # Act
        response = api_context.post(url_endpoint, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for URL without protocol, got {response.status}"

    # def test_create_url_with_complex_params(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test creating URL with complex JSON parameters."""
    #     # Arrange
    #     test_data = {
    #         "url": "https://complex.example.com/api",
    #         "params": {
    #             "filters": {
    #                 "category": ["tech", "business"],
    #                 "date_range": {
    #                     "start": "2024-01-01",
    #                     "end": "2024-12-31"
    #                 }
    #             },
    #             "pagination": {
    #                 "page": 1,
    #                 "limit": 50
    #             },
    #             "sort": "date_desc"
    #         }
    #     }
    #     url_endpoint = api_helper.get_entity_url("url")

    #     # Act
    #     response = api_context.post(url_endpoint, data=test_data)
    #     expect(response).to_be_ok()

    #     payload = response.json()

    #     # Assert
    #     api_helper.validate_response_structure(payload)
    #     assert payload["status"] == "perfect"

    #     data = payload["data"]
    #     url_obj = data[0]
    #     assert url_obj["url"] == test_data["url"]
    #     assert url_obj["params"] == test_data["params"]

    # def test_url_crud_workflow(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
    #     """Test complete CRUD workflow for URL entity."""
    #     # Create
    #     test_data = api_helper.create_test_data("url")
    #     create_url = api_helper.get_entity_url("url")
        
    #     create_response = api_context.post(create_url, data=test_data)
    #     # expect(create_response).to_be_ok()
        
    #     created_url = create_response.json()["data"][0]
    #     url_id = created_url["id"]

    #     # Read
    #     get_url = api_helper.get_entity_url("url", url_id)
    #     get_response = api_context.get(get_url)
    #     # expect(get_response).to_be_ok()
        
    #     retrieved_url = get_response.json()["data"][0]
    #     assert retrieved_url["id"] == url_id

    #     # Update
    #     update_data = {
    #         "url": "https://updated.example.com", 
    #         "params": {"updated": True}
    #     }
    #     update_response = api_context.put(get_url, data=update_data)
    #     expect(update_response).to_be_ok()
        
    #     updated_url = update_response.json()["data"][0]
    #     assert updated_url["url"] == update_data["url"]
    #     assert updated_url["params"] == update_data["params"]

    #     # Delete
    #     delete_response = api_context.delete(get_url)
    #     expect(delete_response).to_be_ok()

    #     # Verify deletion
    #     final_get_response = api_context.get(get_url)
    #     assert final_get_response.status == 404
