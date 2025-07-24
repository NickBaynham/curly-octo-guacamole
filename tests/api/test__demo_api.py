from playwright.sync_api import Playwright, APIRequestContext, expect

def test_fetch_user_data(playwright: Playwright) -> None:
    # Create an API request context
    request_context = playwright.request.new_context()

    # Make a GET request to the API endpoint
    response = request_context.get("https://dummyjson.com/users/1")

    # Assert that the response is successful (status code 2xx)
    expect(response).to_be_ok() 

    # Parse the response body as JSON
    user_data = response.json() 

    # Verify specific data points in the response
    assert user_data["id"] == 1
    assert user_data["firstName"] == "Emily"
    assert user_data["lastName"] == "Johnson"
    assert user_data["age"] == 28

    # You can add more assertions here to verify other fields in the user_data dictionary
    print(f"User data successfully fetched and verified: {user_data}")
