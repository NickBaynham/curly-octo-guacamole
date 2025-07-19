from tests.conftest import get_base_url
import logging
from playwright.sync_api import Page
from tests.conftest import get_base_url

class UserPage:
    def __init__(self, page: Page):
        self.page = page
        self.users_button = page.get_by_role("button", name="Manage Users")
        self.create_user_button = self.page.get_by_role("button", name="Create User")
        self.username_input = self.page.locator("#username")
        self.email_input = self.page.locator("#email")
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.users_management_link = self.page.get_by_text("Users Management")
        self.events_management_link = page.get_by_text("Events Management")

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def create_user(self, user_data: dict):
        """Create a user with the given details."""

        self.log.info("Creating user with data: %s", user_data)    
        self.page.goto(get_base_url())
        self.users_button.click()
        
        # Click the "Create User" button
        self.create_user_button.click()

        # Fill in the user details
        self.page.fill('#username', user_data["username"])
        self.page.fill('#password', user_data["password"])
        self.page.fill('#email', user_data["email"])
        self.page.fill('#firstName', user_data["first_name"])
        self.page.fill('#lastName', user_data["last_name"])
        self.page.select_option('#gender', label = user_data["gender"])
        self.page.fill('#dob', user_data["dob"])
        self.page.fill('#netWorth', str(user_data["net_worth"]))

        # If data is True, check the checkbox; if False, uncheck it
        if user_data["owner"]:
            self.page.check('#isAccountOwner')
        else:
            self.page.uncheck('#isAccountOwner')
        
        self.page.fill('#accountId', user_data["account_id"])
        self.log.info("Filled user details: %s", user_data)

        # Click the "Submit" button to submit the form
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create user")

        # Click the "Events Management" link to return home
        self.events_management_link.click()
