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

# Adding a new Account with today's date in the 'expiredAt' field
with sync_playwright () as playwright:
    logger.info("Starting Playwright example 2 script for %s", website)

    browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    page = browser.new_page()
    page.goto(website)

    # Navigate to Accounts
    accounts_button = page.get_by_role("button", name="Manage Accounts")
    accounts_button.click()
    
    # Click the "Create Account" button
    create_account_button = page.get_by_role("button", name="Create Account")
    create_account_button.click()

    # Enter today's date for the 'expiredAt' field
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    page.fill('#expiredAt', today)  # Assuming the input field has an ID of 'expiredAt'
    logger.info("Filled 'Expired At' field with today's date: %s", today)

    # Click the "Submit" button to submit the form
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    logger.info("Clicked 'Submit' button to create account")

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