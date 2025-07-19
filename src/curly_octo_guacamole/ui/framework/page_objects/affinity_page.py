import logging
from playwright.sync_api import Page
from tests.conftest import get_base_url

class AffinityPage:
    def __init__(self, page: Page):
        self.page = page
        self.affinity_button = page.get_by_role("button", name="Manage Event Affinity")
        self.create_affinity_button = self.page.get_by_role("button", name="Create TagAffinity")
        self.name_input = self.page.locator("#name")  # Assuming the input field has an ID of 'name'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)


    def create_affinity(self, user_data: dict):
        """Create an affinity with the given name."""
        self.page.goto(get_base_url())
        self.affinity_button.click()
        self.create_affinity_button.click()

        # Fill in the user details
        self.page.fill('#tag', user_data["tag"])
        self.page.fill('input[type="number"]', str(user_data["affinity"]))
        self.page.fill('#profileId', user_data["profile_id"])
        self.log.info("Filled affinity details: %s", user_data)

        # Click the "Submit" button to submit the form
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create user")

        # Click the "Events Management" link to return home
        self.events_management_link.click()
