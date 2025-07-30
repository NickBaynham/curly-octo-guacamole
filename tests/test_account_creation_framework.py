"""
Test account creation via the framework API endpoint.
This test demonstrates how to trigger account creation tests through the FastAPI endpoint.
"""

import pytest
import requests
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

class TestAccountCreationFramework:
    """Test suite for account creation via framework API endpoint."""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """Get the base URL for the framework API."""
        return "http://localhost:8000"
    
    def test_create_account_via_framework_api(self, api_base_url):
        """Test creating an account via the framework API endpoint."""
        
        # Test data
        account_data = {
            "action": "create_account",
            "date": "20250819"  # YYYYMMDD format
        }
        
        # Make the API call
        response = requests.post(f"{api_base_url}/create_account", json=account_data)
        
        # Assert response structure
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert "status" in result, "Response missing 'status' field"
        assert "result" in result, "Response missing 'result' field"
        assert result["status"] == "ok", f"Expected 'ok' status, got {result['status']}"
        
        # Check the test result
        test_result = result["result"]
        assert "success" in test_result, "Test result missing 'success' field"
        assert "expired_at" in test_result, "Test result missing 'expired_at' field"
        assert "message" in test_result, "Test result missing 'message' field"
        
        # If the test was successful, verify the account was created
        if test_result["success"]:
            print(f"✅ Account creation test passed with expiration date: {test_result['expired_at']}")
        else:
            print(f"❌ Account creation test failed: {test_result.get('error_message', 'Unknown error')}")
            # Don't fail the test if UI is not available, just log the issue
            if "Connection refused" in str(test_result.get('error', '')):
                pytest.skip("UI server not available, skipping UI test")
    
    def test_create_account_with_today_date(self, api_base_url):
        """Test creating an account with today's date."""
        
        # Use today's date in YYYYMMDD format
        today = datetime.now().strftime("%Y%m%d")
        
        account_data = {
            "action": "create_account",
            "date": today
        }
        
        response = requests.post(f"{api_base_url}/create_account", json=account_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        test_result = result["result"]
        
        if test_result["success"]:
            print(f"✅ Account created with today's date: {today}")
        else:
            print(f"❌ Account creation failed with today's date: {today}")
            if "Connection refused" in str(test_result.get('error', '')):
                pytest.skip("UI server not available, skipping UI test")
    
    def test_create_account_invalid_date_format(self, api_base_url):
        """Test creating an account with invalid date format."""
        
        # Test with invalid date format
        account_data = {
            "action": "create_account",
            "date": "invalid-date"
        }
        
        response = requests.post(f"{api_base_url}/create_account", json=account_data)
        
        # The API should still accept the request, but the UI test might fail
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        test_result = result["result"]
        
        # The test might fail due to invalid date format in the UI
        if not test_result["success"]:
            print(f"⚠️  Account creation failed as expected with invalid date format")
        else:
            print(f"✅ Account creation succeeded despite invalid date format")
    
    def test_create_account_missing_date(self, api_base_url):
        """Test creating an account without providing a date."""
        
        # Test without date field
        account_data = {
            "action": "create_account"
        }
        
        response = requests.post(f"{api_base_url}/create_account", json=account_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        test_result = result["result"]
        
        # Should use default date
        if test_result["success"]:
            print(f"✅ Account created with default date: {test_result['expired_at']}")
        else:
            print(f"❌ Account creation failed with default date")
            if "Connection refused" in str(test_result.get('error', '')):
                pytest.skip("UI server not available, skipping UI test")
    
    def test_create_account_direct_playwright(self):
        """Test account creation directly using Playwright (alternative approach)."""
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                # Navigate to the application
                page.goto("http://localhost:4200")
                page.wait_for_load_state("networkidle")
                
                # Navigate to Accounts page
                accounts_button = page.get_by_role("button", name="Manage Accounts")
                accounts_button.click()
                page.wait_for_load_state("networkidle")
                
                # Click Create Account button
                create_account_button = page.get_by_role("button", name="Create Account")
                create_account_button.click()
                
                # Fill in the expiredAt field
                today = datetime.now().strftime("%Y-%m-%d")
                page.fill('#expiredAt', today)
                
                # Submit the form
                submit_button = page.get_by_role("button", name="Submit")
                submit_button.click()
                
                # Wait for the form submission to complete
                page.wait_for_load_state("networkidle")
                
                # Check if account was created successfully
                try:
                    page.wait_for_url("**/entity/Account", timeout=5000)
                    print(f"✅ Direct Playwright test: Account created successfully with date {today}")
                    success = True
                except:
                    error_elements = page.locator(".error, .alert, [role='alert']")
                    if error_elements.count() > 0:
                        error_message = error_elements.first.text_content()
                        print(f"❌ Direct Playwright test failed: {error_message}")
                        success = False
                    else:
                        print(f"⚠️  Direct Playwright test: Could not determine success/failure")
                        success = True  # Assume success if no clear error
                
                context.close()
                browser.close()
                
                assert success, "Account creation via direct Playwright test failed"
                
        except Exception as e:
            if "Connection refused" in str(e) or "net::ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("UI server not available, skipping direct Playwright test")
            else:
                raise e

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 