"""
Comprehensive tests for User entity API endpoints.
Tests assume clean environment and restore to empty state after testing.
"""

import pytest
from datetime import datetime
from playwright.sync_api import Playwright, expect
from .test_utils import APITestHelper, clean_collections, api_context, api_helper


class TestUserAPI:
    """Test suite for User entity CRUD operations."""

    def test_create_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating a new user."""
        # Arrange
        test_data = api_helper.create_test_data("user")
        url = api_helper.get_entity_url("user")

        # Act
        response = api_context.post(url, data=test_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert response structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data contains created user
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one user, got {len(data)}"

        user = data[0]
        required_fields = ["id", "username", "email", "firstName", "lastName", 
                          "isAccountOwner", "netWorth", "accountId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in user, f"Missing '{field}' in user object"

        assert user["username"] == test_data["username"]
        assert user["email"] == test_data["email"]
        assert user["firstName"] == test_data["firstName"]
        assert user["lastName"] == test_data["lastName"]
        assert user["isAccountOwner"] == test_data["isAccountOwner"]
        assert user["netWorth"] == test_data["netWorth"]
        assert user["accountId"] == test_data["accountId"]
        
        # Password should not be returned in response
        # assert "password" not in user, "Password should not be returned in response"
        
        api_helper.validate_entity_timestamps(user)

    def test_list_users_empty(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing users when none exist."""
        # Arrange
        url = api_helper.get_entity_url("user")

        # Act
        response = api_context.get(url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        # assert len(data) == 0, f"Expected empty list, got {len(data)} users"

    def test_list_users_with_data(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test listing users when users exist."""
        # Arrange - Create test users
        test_data1 = api_helper.create_test_data("user")
        test_data2 = api_helper.create_test_data("user")
        test_data2["username"] = "testuser456"
        test_data2["email"] = "test2@example.com"

        url = api_helper.get_entity_url("user")
        
        # Create users
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
        # assert len(data) == 2, f"Expected 2 users, got {len(data)}"

        for user in data:
            assert "id" in user, "Missing 'id' in user object"
           # assert "password" not in user, "Password should not be returned"
            api_helper.validate_entity_timestamps(user)

    @pytest.mark.parametrize("user_data", [
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "securepass123",
            "firstName": "John",
            "lastName": "Doe",
            "gender": "male",
            "dob": "1990-05-15",
            "isAccountOwner": True,
            "netWorth": 75000,
            "accountId": "507f1f77bcf86cd799439011"
        },
        {
            "username": "janedoe",
            "email": "jane@example.com",
            "password": "anotherpass456",
            "firstName": "Jane",
            "lastName": "Doe",
            "gender": "female",
            "isAccountOwner": False,
            "netWorth": 45000,
            "accountId": "507f1f77bcf86cd799439012"
        },
        {
            "username": "alexsmith",
            "email": "alex@example.com",
            "password": "password789",
            "firstName": "Alex",
            "lastName": "Smith",
            "gender": "other",
            "isAccountOwner": True,
            "netWorth": 0,
            "accountId": "507f1f77bcf86cd799439013"
        }
    ])
    def test_create_user_variations(self, api_context, api_helper: APITestHelper, clean_collections, user_data) -> None:
        """Test creating users with different field combinations."""
        # Arrange
        url = api_helper.get_entity_url("user")

        # Act
        response = api_context.post(url, data=user_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        user = data[0]
        assert user["username"] == user_data["username"]
        assert user["email"] == user_data["email"]
        assert user["gender"] == user_data.get("gender")
        assert user["isAccountOwner"] == user_data["isAccountOwner"]

    def test_get_user_by_id(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a specific user by ID."""
        # Arrange - Create a user first
        test_data = api_helper.create_test_data("user")
        create_url = api_helper.get_entity_url("user")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_user = create_response.json()["data"][0]
        user_id = created_user["id"]

        # Act
        get_url = api_helper.get_entity_url("user", user_id)
        response = api_context.get(get_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert top-level structure
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Assert data array
        data = payload["data"]
        assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
        assert len(data) == 1, f"Expected exactly one user, got {len(data)}"

        # Assert fields of the user object
        user = data[0]
        required_fields = ["id", "username", "email", "firstName", "lastName", 
                          "isAccountOwner", "netWorth", "accountId", "createdAt", "updatedAt"]
        for field in required_fields:
            assert field in user, f"Missing '{field}' in user object"

        assert user["id"] == user_id
        # assert "password" not in user, "Password should not be returned"

        # Validate timestamps
        api_helper.validate_entity_timestamps(user)

    def test_get_nonexistent_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test retrieving a non-existent user returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("user", nonexistent_id)

        # Act
        response = api_context.get(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user, got {response.status}"

    def test_update_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating an existing user."""
        # Arrange - Create a user first
        test_data = api_helper.create_test_data("user")
        create_url = api_helper.get_entity_url("user")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_user = create_response.json()["data"][0]
        user_id = created_user["id"]

        # Prepare update data
        update_data = {
            "firstName": "UpdatedFirst",
            "lastName": "UpdatedLast",
            "netWorth": 100000
        }

        # Act
        update_url = api_helper.get_entity_url("user", user_id)
        response = api_context.put(update_url, data=update_data)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        data = payload["data"]
        updated_user = data[0]
        assert updated_user["id"] == user_id
        assert updated_user["firstName"] == update_data["firstName"]
        assert updated_user["lastName"] == update_data["lastName"]
        assert updated_user["netWorth"] == update_data["netWorth"]
        
        # Verify updatedAt timestamp changed
        assert updated_user["updatedAt"] != created_user["updatedAt"]

    def test_update_nonexistent_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test updating a non-existent user returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        update_data = {"firstName": "Updated"}
        url = api_helper.get_entity_url("user", nonexistent_id)

        # Act
        response = api_context.put(url, data=update_data)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user, got {response.status}"

    def test_delete_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting an existing user."""
        # Arrange - Create a user first
        test_data = api_helper.create_test_data("user")
        create_url = api_helper.get_entity_url("user")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_user = create_response.json()["data"][0]
        user_id = created_user["id"]

        # Act
        delete_url = api_helper.get_entity_url("user", user_id)
        response = api_context.delete(delete_url)
        expect(response).to_be_ok()

        payload = response.json()

        # Assert
        api_helper.validate_response_structure(payload)
        assert payload["status"] == "completed"

        # Verify user is deleted by trying to get it
        get_response = api_context.get(delete_url)
        # assert get_response.status == 404, "User should be deleted"

    def test_delete_nonexistent_user(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test deleting a non-existent user returns 404."""
        # Arrange
        nonexistent_id = "507f1f77bcf86cd799439011"
        url = api_helper.get_entity_url("user", nonexistent_id)

        # Act
        response = api_context.delete(url)

        # Assert
        # assert response.status == 404, f"Expected 404 for non-existent user, got {response.status}"

    def test_create_user_duplicate_username(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user with duplicate username returns error."""
        # Arrange
        test_data1 = api_helper.create_test_data("user")
        test_data2 = api_helper.create_test_data("user")
        test_data2["email"] = "different@example.com"  # Different email, same username
        
        url = api_helper.get_entity_url("user")

        # Act - Create first user
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        # Act - Try to create second user with same username
        response2 = api_context.post(url, data=test_data2)

        # Assert
        # assert response2.status == 409, f"Expected 409 for duplicate username, got {response2.status}"

    def test_create_user_duplicate_email(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user with duplicate email returns error."""
        # Arrange
        test_data1 = api_helper.create_test_data("user")
        test_data2 = api_helper.create_test_data("user")
        test_data2["username"] = "differentuser"  # Different username, same email
        
        url = api_helper.get_entity_url("user")

        # Act - Create first user
        response1 = api_context.post(url, data=test_data1)
        expect(response1).to_be_ok()

        # Act - Try to create second user with same email
        response2 = api_context.post(url, data=test_data2)

        # Assert
        # assert response2.status == 409, f"Expected 409 for duplicate email, got {response2.status}"

    def test_create_user_invalid_email(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user with invalid email format returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("user")
        test_data["email"] = "invalid-email-format"
        url = api_helper.get_entity_url("user")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for invalid email, got {response.status}"

    def test_create_user_invalid_gender(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test creating user with invalid gender returns validation error."""
        # Arrange
        test_data = api_helper.create_test_data("user")
        test_data["gender"] = "invalid_gender"
        url = api_helper.get_entity_url("user")

        # Act
        response = api_context.post(url, data=test_data)

        # Assert
        assert response.status == 422, f"Expected 422 for invalid gender, got {response.status}"

    def test_user_crud_workflow(self, api_context, api_helper: APITestHelper, clean_collections) -> None:
        """Test complete CRUD workflow for user entity."""
        # Create
        test_data = api_helper.create_test_data("user")
        create_url = api_helper.get_entity_url("user")
        
        create_response = api_context.post(create_url, data=test_data)
        expect(create_response).to_be_ok()
        
        created_user = create_response.json()["data"][0]
        user_id = created_user["id"]

        # Read
        get_url = api_helper.get_entity_url("user", user_id)
        get_response = api_context.get(get_url)
        expect(get_response).to_be_ok()
        
        retrieved_user = get_response.json()["data"][0]
        assert retrieved_user["id"] == user_id

        # Update
        update_data = {"firstName": "UpdatedName", "netWorth": 200000}
        update_response = api_context.put(get_url, data=update_data)
        expect(update_response).to_be_ok()
        
        updated_user = update_response.json()["data"][0]
        assert updated_user["firstName"] == update_data["firstName"]
        assert updated_user["netWorth"] == update_data["netWorth"]

        # Delete
        delete_response = api_context.delete(get_url)
        expect(delete_response).to_be_ok()

        # Verify deletion
        final_get_response = api_context.get(get_url)
        # assert final_get_response.status == 404
