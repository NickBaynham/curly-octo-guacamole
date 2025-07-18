from playwright.sync_api import Page

from tests.conftest import get_base_url

class AffinityPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto(get_base_url())
        self.create_affinity_button = self.page.get_by_role("button", name="Create Affinity")
        self.name_input = self.page.locator("#name")  # Assuming the input field has an ID of 'name'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")

    def create_affinity(self, user_data: dict):
        """Create an affinity with the given name."""
        self.create_affinity_button.click()
        self.name_input.fill(user_data["name"])
        self.submit_button.click()
        self.events_management_link.click()  # Return to the main page after creating the affinity