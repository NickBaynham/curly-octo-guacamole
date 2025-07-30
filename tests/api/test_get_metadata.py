from playwright.sync_api import Playwright, expect

def test_fetch_user_data(playwright: Playwright) -> None:
    # Configuration
    API_ROOT = "http://localhost:5500"
    API_METADATA = f"{API_ROOT}/api/metadata"

    # Create an API request context
    request_context = playwright.request.new_context()

    # Make a GET request to the API endpoint
    response = request_context.get(API_METADATA)
    print(response)  # <APIResponse ... status=200>

    # Assert that the response is successful (status code 2xx)
    expect(response).to_be_ok()  # <-- note the ()

    # Deserialize into a Python dict
    metadata = response.json()

    # Now use plain assertions for dict content
    field_names = ["projectName", "database", "entities"]
    assert isinstance(metadata, dict), "Response is not a dictionary"
    assert all(field in metadata for field in field_names), "Missing fields in metadata"
    assert isinstance(metadata["projectName"], str), "projectName should be astring"
    assert isinstance(metadata["database"], str), "description should be a string"
    assert isinstance(metadata["entities"], dict), "entities should be a dictionary"
    assert "projectName" in metadata,      "Missing 'projectName' in metadata"

    assert metadata["projectName"] == "Events", "Project name does not match expected value"
    print("Metadata fetched successfully:", metadata)
    request_context.dispose()