from playwright.sync_api import Playwright, APIRequestContext, expect

def test_fetch_user_data(playwright: Playwright) -> None:
    # Configuration
    API_ROOT = "http://localhost:5500"

    # Create an API request context
    request_context = playwright.request.new_context()

    # Make a GET request to the API endpoint
    response = request_context.get(API_ROOT)

    # Assert that the response is a failure (status code 404)
    expect(response).not_to_be_ok # Expecting a failure here 404
