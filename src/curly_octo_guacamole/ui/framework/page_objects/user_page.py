from playwright.sync_api import Page

from tests.conftest import get_base_url

class UserPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(get_base_url())
        self.create_user_button = self.page.get_by_role("button", name="Create User")
        self.username_input = self.page.locator("#username")
        self.email_input = self.page.locator("#email")
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.users_management_link = self.page.get_by_text("Users Management")

    def create_user(self, user_data: dict):
        self.create_user_button.click()
        self.username_input.fill(user_data["username"])
        self.email_input.fill(user_data["email"])
        self.submit_button.click()
        self.users_management_link.click()
