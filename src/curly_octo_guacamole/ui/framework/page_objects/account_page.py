from playwright.sync_api import Page

from tests.conftest import get_base_url

class AccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(get_base_url())
        self.create_account_button = self.page.get_by_role("button", name="Create Account")
        self.expired_at_input = self.page.locator("#expiredAt")  # Assuming the input field has an ID of 'expiredAt'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")

    def create_account(self, user_data: dict):
        """Create an account with the given expiration date."""
        self.create_account_button.click()
        self.expired_at_input.fill(user_data["expired_at"])
        self.submit_button.click()
        self.events_management_link.click()  # Return to the main page after creating the account