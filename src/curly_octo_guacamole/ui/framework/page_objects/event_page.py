import logging
from playwright.sync_api import Page

from tests.conftest import get_base_url

class EventPage:
    def __init__(self, page: Page):
        self.page = page
        self.events_button = page.get_by_role("button", name="Manage Events")
        self.create_event_button = self.page.get_by_role("button", name="Create Event")
        self.url_input = self.page.locator("#url")
        self.title_input = self.page.locator("#title")
        self.date_time_input = self.page.locator("#dateTime")
        self.location_input = self.page.locator("#location")
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)


    def create_event(self, user_data: dict):
        """Create an event with the given details."""

        self.page.goto(get_base_url())
        self.events_button.click()
        self.create_event_button.click()

        # Fill in the user details
        self.page.fill('#url', user_data["url"])
        self.page.fill('#title', user_data["title"])
        self.page.fill('#dateTime', user_data["date_time"])
        self.page.fill('#location', user_data["location"])
        self.log.info("Filled user details: %s", user_data)

        # Click the "Submit" button to submit the form
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create event")

        # Click the "Events Management" link to return home
        self.events_management_link.click()
