import logging
from playwright.sync_api import Page
import pytest

def test_create_entities(page: Page, base_url: str, log: logging.Logger):
    """Test creating entities using the UI"""
    
    # Navigate to the base URL
    page.goto(base_url)
    
    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")
    
    # Check if the title is correct
    assert page.title() == "Events Management"
    
    #############################################
    # Accounts
    #############################################

    accounts_button = page.get_by_role("button", name="Manage Accounts")
    assert accounts_button.is_visible(), "Manage Accounts button is not visible"
    accounts_button.click()
    
    # Wait for the new page to load
    page.wait_for_load_state("networkidle")
    
    # Verify the new URL
    assert page.url == base_url + "/entity/Account"
    
    # Verify the title of the new page
    page_title = page.get_by_text("Accounts")
    assert page_title.is_visible(), "Accounts page title is not visible"

        # Click the "Create Account" button
    create_account_button = page.get_by_role("button", name="Create Account")
    create_account_button.click()

    # Enter today's date for the 'expiredAt' field
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    page.fill('#expiredAt', today)  # Assuming the input field has an ID of 'expiredAt'
    log.info("Filled 'Expired At' field with today's date: %s", today)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create account")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    #############################################
    # Users
    #############################################

    # User data
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "nobody@nowhere.com",
        "first_name": "Test",
        "last_name": "User",
        "gender": "female",
        "dob": "1990-01-01",
        "owner": False,
        "net_worth": 1000000,
        "account_id": "6871326a0e46574d4becf423",
    }

    # Navigate to Users
    users_button = page.get_by_role("button", name="Manage Users")
    users_button.click()
    
    # Click the "Create User" button
    create_user_button = page.get_by_role("button", name="Create User")
    create_user_button.click()

    # Fill in the user details
    page.fill('#username', user_data["username"])
    page.fill('#password', user_data["password"])
    page.fill('#email', user_data["email"])
    page.fill('#firstName', user_data["first_name"])
    page.fill('#lastName', user_data["last_name"])
    page.select_option('#gender', label = user_data["gender"])
    page.fill('#dob', user_data["dob"])
    page.fill('#netWorth', str(user_data["net_worth"]))
    # If data is True, check the checkbox; if False, uncheck it
    if user_data["owner"]:
        page.check('#isAccountOwner')
    else:
        page.uncheck('#isAccountOwner')
    page.fill('#accountId', user_data["account_id"])
    log.info("Filled user details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create user")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    #############################################
    # Events
    #############################################

    user_data = {
        "url": "https://url.com",
        "title": "this is a title",
        "date_time": "2025-01-01",
        "location": "444 Event Drive, Anytown, CA 90102",
    }

    # Navigate to Events
    events_button = page.get_by_role("button", name="Manage Events")
    events_button.click()
    
    # Click the "Create Event" button
    create_event_button = page.get_by_role("button", name="Create Event")
    create_event_button.click()

    # Fill in the user details
    page.fill('#url', user_data["url"])
    page.fill('#title', user_data["title"])
    page.fill('#dateTime', user_data["date_time"])
    page.fill('#location', user_data["location"])
    log.info("Filled user details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create event")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    #############################################
    # Profiles
    #############################################

    user_data = {
        "name": "profile 1",
        "user_id": "nobody@nowhere.com",
        "radius_miles": 100,
    }

    # Navigate to Users
    profiles_button = page.get_by_role("button", name="Manage User Profiles")
    profiles_button.click()
    
    # Click the "Create Profile" button
    create_profile_button = page.get_by_role("button", name="Create Profile")
    create_profile_button.click()

    # Fill in the user details
    page.fill('#name', user_data["name"])
    page.fill('#userId', user_data["user_id"])
    page.fill('input[type="number"]', str(user_data["radius_miles"]))

    log.info("Filled profile details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create user")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    #############################################
    # Affinities
    #############################################

    user_data = {
        "tag": "tag 1",
        "affinity": 1,
        "profile_id": "68713c4c0e46574d4becf437",
    }

    # Navigate to Tag Affinity
    affinity_button = page.get_by_role("button", name="Manage Event Affinity")
    affinity_button.click()
    
    # Click the "Create TagAffinity" button
    create_profile_button = page.get_by_role("button", name="Create TagAffinity")
    create_profile_button.click()

    # Fill in the user details
    page.fill('#tag', user_data["tag"])
    page.fill('input[type="number"]', str(user_data["affinity"]))
    page.fill('#profileId', user_data["profile_id"])

    log.info("Filled affinity details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create user")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    #############################################
    # User Events
    #############################################

    user_data = {
        "attended": True,
        "rating": 5,
        "event_id": "68713f650e46574d4becf43c",
        "user_id": "687133d20e46574d4becf424",
    }

    # Navigate to Event Attendance
    attendance_button = page.get_by_role("button", name="Manage Event Attendance")
    attendance_button.click()
    
    # Click the "Create UserEvent" button
    create_user_event_button = page.get_by_role("button", name="Create UserEvent")
    create_user_event_button.click()

    # Fill in the user event attended value
    if user_data["attended"]:
        page.check('#attended')
    else:
        page.uncheck('#attended')

    page.fill('input[type="number"]', str(user_data["rating"]))
    page.fill('#eventId', user_data["event_id"])
    page.fill('#userId', user_data["user_id"])
    log.info("Filled user details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    log.info("Clicked 'Submit' button to create event")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()


@pytest.fixture(scope="session")
def log():

    """Fixture to set up logging for the tests."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the application."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv("BASE_URL", "http://localhost:4200")

# pdm run pytest tests/ui/test_simple_navigation.py --log-cli-level=INFO --headed --slomo=500
# Configuration is set in pytest.ini - but is overridden by .env is present
