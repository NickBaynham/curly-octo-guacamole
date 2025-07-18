from calendar import c
from playwright.sync_api import Page

from tests.conftest import get_base_url

class ProfilePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(get_base_url())
        self.profile_button = self.page.get_by_role("button", name="Profile")
        self.username_input = self.page.locator("#username")  # Assuming the input field has an ID of 'username'
        self.email_input = self.page.locator("#email")  # Assuming the input field has an ID of 'email'
        self.save_button = self.page.get_by_role("button", name="Save")
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.events_management_link = self.page.get_by_text("Events Management")

    def create_profile(self, user_data: dict):
        """Create a profile with the given user data."""
        self.profile_button.click()
        self.username_input.fill(user_data["username"])
        self.email_input.fill(user_data["email"])
        self.save_button.click()
        self.events_management_link.click()
