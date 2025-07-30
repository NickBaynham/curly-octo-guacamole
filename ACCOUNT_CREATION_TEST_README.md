# Account Creation Test Framework

This document explains how to use the new account creation test functionality that integrates with the FastAPI framework endpoint.

## Overview

The account creation test allows you to trigger Playwright-based UI tests through a REST API endpoint. This provides a way to programmatically test account creation functionality.

## Components

### 1. FastAPI Endpoint (`app/main.py`)
- **Endpoint**: `POST /create_account`
- **Request Body**: 
  ```json
  {
    "action": "create_account",
    "date": "20250819"  // YYYYMMDD format
  }
  ```
- **Response**: 
  ```json
  {
    "status": "ok",
    "result": {
      "success": true,
      "expired_at": "2025-08-19",
      "error_message": null,
      "message": "Account creation test completed"
    }
  }
  ```

### 2. Playwright Runner (`tests/playwright_runner.py`)
- Handles the `create_account` keyword
- Launches a headless browser
- Navigates to the UI application
- Creates an account with the specified expiration date
- Returns test results

### 3. Test Scripts
- `test_account_creation.py`: Simple script to test the endpoint
- `tests/test_account_creation_framework.py`: Comprehensive pytest tests

## Usage

### Running the FastAPI Server

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

### Testing via Command Line

```bash
# Run the simple test script
python test_account_creation.py

# Run the comprehensive pytest tests
pdm run pytest tests/test_account_creation_framework.py -v
```

### Testing via HTTP Request

```bash
# Using curl
curl -X POST http://localhost:8000/create_account \
  -H "Content-Type: application/json" \
  -d '{"action": "create_account", "date": "20250819"}'

# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/create_account",
    json={"action": "create_account", "date": "20250819"}
)
print(response.json())
```

## Test Scenarios

### 1. Basic Account Creation
- Creates an account with a specified expiration date
- Validates the UI form submission
- Checks for successful account creation

### 2. Date Format Handling
- Supports YYYYMMDD format in the API
- Converts to YYYY-MM-DD format for UI input
- Handles missing dates with defaults

### 3. Error Handling
- Gracefully handles UI server unavailability
- Provides detailed error messages
- Skips tests when UI is not accessible

## Prerequisites

1. **UI Application**: The Angular/React application must be running on `http://localhost:4200`
2. **FastAPI Server**: The framework API must be running on `http://localhost:8000`
3. **Playwright**: Browser automation dependencies must be installed

## Example Test Flow

1. **API Request**: Send POST to `/create_account` with test data
2. **Playwright Execution**: 
   - Launch headless browser
   - Navigate to `http://localhost:4200`
   - Click "Manage Accounts" button
   - Click "Create Account" button
   - Fill in expiration date
   - Submit form
3. **Result Validation**: Check for successful navigation or error messages
4. **Response**: Return structured result with success/failure status

## Error Scenarios

- **UI Server Down**: Returns error with connection details
- **Invalid Date Format**: May fail in UI but API accepts request
- **Missing Date**: Uses default date (2025-08-19)
- **Form Errors**: Captures and reports UI validation errors

## Integration with Existing Tests

This framework integrates with the existing test infrastructure:
- Uses the same Playwright setup as other UI tests
- Follows the same patterns as existing account tests
- Can be extended for other entity types (users, events, etc.)

## Future Enhancements

1. **Additional Entities**: Extend to support user, event, and other entity creation
2. **Validation Testing**: Add more comprehensive validation scenarios
3. **Performance Testing**: Add load testing capabilities
4. **Reporting**: Enhanced test result reporting and analytics 