from playwright.sync_api import Page

from tests.conftest import get_base_url

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.title = self.page.title()
        self.accounts_button = self.page.get_by_role("button", name="Manage Accounts")


    def go_home(self):
        """Navigate to the home page."""
        self.page.goto(get_base_url())
        self.page.wait_for_load_state("networkidle")
        assert self.title == "Events Management", "Title does not match expected value"
        return self.page

    def go_accounts(self):
        """Navigate to the accounts page."""
        self.accounts_button.click()
        self.page.wait_for_load_state("networkidle")
        assert self.page.url == get_base_url() + "/entity/Account", "URL does not match expected value"
        assert self.page.get_by_text("Accounts").is_visible(), "Accounts page title is not visible"
        return self.page