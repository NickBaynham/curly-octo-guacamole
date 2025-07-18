import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()  # Console output
    ]
)

logger = logging.getLogger(__name__)

headless = False
slow_mo = 5000
website = "http://localhost:4200"

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

# Adding a new Account with today's date in the 'expiredAt' field
with sync_playwright () as playwright:
    logger.info("Starting Playwright example 2 script for %s", website)

    browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    page = browser.new_page()
    page.goto(website)

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
    logger.info("Filled user details: %s", user_data)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    logger.info("Clicked 'Submit' button to create user")

    # Click the "Events Management" link to return home
    events_management_link = page.get_by_text("Events Management")
    events_management_link.click()

    page.close()
    browser.close()

    # pdm run src/curly_octo_guacamole/ui/examples/example_2.py
    # This script demonstrates how to use Playwright to launch a browser,
    # navigate to a specific URL, and then close the browser.
    # It uses the sync API for simplicity.
    # The `sync_playwright` function is used to start Playwright,
    # and the `chromium.launch` method is used to launch a Chromium browser instance.
    # The `headless` option is set to True to run the browser in headless mode,
    # and the `slow_mo` option is set to 0 milliseconds for normal speed.
    # After navigating to the specified URL, the script closes the page and the browser.
    # This is a basic example of using Playwright for browser automation.
    # The script can be extended with more complex interactions,
    # such as clicking buttons, filling forms, and verifying page content.
    # Playwright's capabilities allow for comprehensive browser automation,
    # making it suitable for end-to-end testing and web scraping tasks.
    # The script can be run in a Python environment with Playwright installed.
    # Ensure you have Playwright installed with `pdm add playwright`