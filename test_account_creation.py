#!/usr/bin/env python3
"""
Test script to demonstrate account creation via the framework API endpoint.
This script shows how to call the /create_account endpoint with test data.
"""

import requests
import json
from datetime import datetime

def test_create_account():
    """Test creating an account via the framework API endpoint."""
    
    # Test data for account creation
    account_data = {
        "action": "create_account",
        "date": "2025-08-19"  # YYYYMMDD format
    }
    
    # API endpoint URL
    url = "http://localhost:8000/create_account"
    
    try:
        # Make the POST request
        response = requests.post(url, json=account_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Check if the test was successful
            if "result" in result and "success" in result["result"]:
                if result["result"]["success"]:
                    print("✅ Account creation test PASSED")
                else:
                    print("❌ Account creation test FAILED")
                    if "error_message" in result["result"]:
                        print(f"Error: {result['result']['error_message']}")
            else:
                print("⚠️  Unexpected response format")
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the FastAPI server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_create_account_with_custom_date():
    """Test creating an account with a custom expiration date."""
    
    # Use today's date in YYYYMMDD format
    today = datetime.now().strftime("%Y%m%d")
    
    account_data = {
        "action": "create_account",
        "date": today
    }
    
    url = "http://localhost:8000/create_account"
    
    try:
        response = requests.post(url, json=account_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Custom date test response: {json.dumps(result, indent=2)}")
            
            if "result" in result and result["result"].get("success"):
                print(f"✅ Account created with expiration date: {today}")
            else:
                print(f"❌ Account creation failed with date: {today}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing account creation via framework API endpoint...")
    print("=" * 60)
    
    print("\n1. Testing with default date (2025-08-19):")
    test_create_account()
    
    print("\n2. Testing with today's date:")
    test_create_account_with_custom_date()
    
    print("\n" + "=" * 60)
    print("Test completed!") 