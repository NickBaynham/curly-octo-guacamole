"""
Test utilities for API testing with MongoDB cleanup functionality.
"""

import pytest
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from playwright.sync_api import Playwright, APIRequestContext

class MongoDBCleaner:
    """Utility class for cleaning up MongoDB collections during testing."""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017", db_name: str = "events_test"):
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
    
    def connect(self):
        """Connect to MongoDB."""
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
    
    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
    
    def clean_all_collections(self):
        """Remove all documents from all collections."""
        if self.db is None:
            self.connect()
        
        collections = [
            "accounts", "users", "profiles", "tagaffinities", 
            "events", "userevents", "urls", "crawls"
        ]
        
        for collection_name in collections:
            try:
                result = self.db[collection_name].delete_many({})
                print(f"Cleaned collection: {collection_name}")
            except Exception as e:
                print(f"Warning: Could not clean collection {collection_name}: {e}")
    
    def clean_collection(self, collection_name: str):
        """Remove all documents from a specific collection."""
        if self.db is None:
            self.connect()
        
        try:
            result = self.db[collection_name].delete_many({})
            print(f"Cleaned {result.deleted_count} documents from {collection_name}")
        except Exception as e:
            print(f"Warning: Could not clean collection {collection_name}: {e}")


class APITestHelper:
    """Helper class for API testing operations."""
    
    def __init__(self, base_url: str = "http://localhost:5500"):
        self.base_url = base_url
    
    def get_entity_url(self, entity_name: str, entity_id: Optional[str] = None) -> str:
        """Get the full URL for an entity endpoint."""
        url = f"{self.base_url}/api/{entity_name.lower()}"
        if entity_id:
            url += f"/{entity_id}"
        return url
    
    @staticmethod
    def validate_response_structure(payload: Dict[str, Any]) -> None:
        """Validate the standard API response structure."""
        assert isinstance(payload, dict), f"Expected JSON object, got {type(payload)}"
        
        required_keys = ("data", "message", "level", "metadata", "notifications", "status", "summary")
        for key in required_keys:
            assert key in payload, f"Missing top-level key: {key}"
    
    @staticmethod
    def validate_entity_timestamps(entity: Dict[str, Any]) -> None:
        """Validate entity timestamp fields."""
        from datetime import datetime
        
        for ts_key in ("createdAt", "updatedAt"):
            if ts_key in entity:
                ts = entity[ts_key]
                assert isinstance(ts, str), f"{ts_key} should be a string"
                try:
                    datetime.fromisoformat(ts)
                except Exception:
                    pytest.fail(f"{ts_key} is not valid ISO datetime: {ts}")
    
    @staticmethod
    def create_test_data(entity_type: str) -> Dict[str, Any]:
        """Create test data for different entity types."""
        test_data = {
            "account": {
                "expiredAt": None
            },
            "user": {
                "username": "testuser123",
                "email": "test@example.com",
                "password": "testpassword123",
                "firstName": "Test",
                "lastName": "User",
                "gender": "other",
                "isAccountOwner": True,
                "netWorth": 50000,
                "accountId": "507f1f77bcf86cd799439011"  # Valid ObjectId format
            },
            "profile": {
                "name": "Test Profile",
                "preferences": "Test preferences",
                "radiusMiles": 25,
                "userId": "507f1f77bcf86cd799439011"
            },
            "tagaffinity": {
                "tag": "technology",
                "affinity": 75,
                "profileId": "507f1f77bcf86cd799439011"
            },
            "event": {
                "url": "https://example.com/event",
                "title": "Test Event",
                "dateTime": "2024-12-01T18:00:00Z",
                "location": "Test Location",
                "cost": 25.50,
                "numOfExpectedAttendees": 100,
                "recurrence": "weekly",
                "tags": ["technology", "networking"]
            },
            "userevent": {
                "attended": True,
                "rating": 4,
                "note": "Great event!",
                "userId": "507f1f77bcf86cd799439011",
                "eventId": "507f1f77bcf86cd799439011"
            },
            "url": {
                "url": "https://example.com/events",
                "params": {"category": "tech", "location": "city"}
            },
            "crawl": {
                "lastParsedDate": "2024-01-15T10:30:00Z",
                "parseStatus": {"status": "success", "items_found": 5},
                "errorsEncountered": [],
                "urlId": "507f1f77bcf86cd799439011"
            }
        }
        
        return test_data.get(entity_type.lower(), {})


@pytest.fixture(scope="session")
def mongodb_cleaner():
    """Pytest fixture for MongoDB cleanup."""
    cleaner = MongoDBCleaner()
    cleaner.connect()
    
    # Clean before tests start
    cleaner.clean_all_collections()
    
    yield cleaner
    
    # Clean after tests complete
    cleaner.clean_all_collections()
    cleaner.disconnect()


@pytest.fixture(scope="function")
def clean_collections(mongodb_cleaner):
    """Pytest fixture to clean collections before each test."""
    mongodb_cleaner.clean_all_collections()
    yield
    # Clean after each test as well
    mongodb_cleaner.clean_all_collections()


@pytest.fixture(scope="session")
def api_helper():
    """Pytest fixture for API test helper."""
    return APITestHelper()


@pytest.fixture(scope="function")
def api_context(playwright: Playwright):
    """Pytest fixture for Playwright API request context."""
    context = playwright.request.new_context()
    yield context
    context.dispose()


def wait_for_api_ready(base_url: str = "http://localhost:5500", timeout: int = 30) -> bool:
    """Wait for the API server to be ready."""
    import time
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/api/metadata", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    return False
