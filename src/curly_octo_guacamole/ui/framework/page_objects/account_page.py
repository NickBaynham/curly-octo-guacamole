from datetime import datetime
import logging
from playwright.sync_api import Page
from tests.conftest import get_base_url

class AccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.accounts_button = self.page.get_by_role("button", name="Manage Accounts")
        self.create_account_button = self.page.get_by_role("button", name="Create Account")
        self.expired_at_input = self.page.locator("#expiredAt")  # Assuming the input field has an ID of 'expiredAt'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")
        self.url = get_base_url() + "/entity/Account"
        self.title = self.page.get_by_text("Accounts")
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def create_account(self, user_data: dict):
        """Create an account with the given expiration date."""

        self.page.goto(get_base_url())
        assert self.accounts_button.is_visible(), "Manage Accounts button is not visible"
        self.accounts_button.click()
        
        # Wait for the new page to load
        self.page.wait_for_load_state("networkidle")
        
        # Verify the new URL
        assert self.page.url == self.url, "URL does not match expected value"
        
        # Verify the title of the new page
        assert self.title.is_visible(), "Accounts page title is not visible"

        # Click the "Create Account" button
        self.create_account_button.click()

        # Enter today's date for the 'expiredAt' field
        today = datetime.now().strftime("%Y-%m-%d")
        self.page.fill('#expiredAt', today)
        self.log.info("Filled 'Expired At' field with today's date: %s", today)

        # Click the "Submit" button to submit the form
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create account")

        # Click the "Events Management" link to return home
        self.events_management_link.click()
