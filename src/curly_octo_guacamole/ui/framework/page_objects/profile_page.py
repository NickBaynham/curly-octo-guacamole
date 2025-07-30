from calendar import c
import logging
from playwright.sync_api import Page

from tests.conftest import get_base_url

class ProfilePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(get_base_url())
        self.profile_button = self.page.get_by_role("button", name="Profile")
        self.create_profile_button = page.get_by_role("button", name="Create Profile")
        self.username_input = self.page.locator("#username")  # Assuming the input field has an ID of 'username'
        self.email_input = self.page.locator("#email")  # Assuming the input field has an ID of 'email'
        self.submit_button = page.get_by_role("button", name="Submit")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.events_management_link = self.page.get_by_text("Events Management")

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def create_profile(self, user_data: dict):
        """Create a profile with the given user data."""
        self.page.goto(get_base_url())
        self.profile_button.click()
        self.create_profile_button.click()

        # Fill in the user details
        self.page.fill('#name', user_data["name"])
        self.page.fill('#userId', user_data["user_id"])
        self.page.fill('input[type="number"]', str(user_data["radius_miles"]))
        self.log.info("Filled profile details: %s", user_data)
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create user")
        self.events_management_link.click()
