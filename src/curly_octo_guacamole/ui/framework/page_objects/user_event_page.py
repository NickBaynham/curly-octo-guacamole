from playwright.sync_api import Page
from tests.conftest import get_base_url

class UserEventPage:
    def __init__(self, page: Page):
        self.page = page
        base_url = get_base_url()
        self.page.goto(get_base_url())
        self.create_event_button = self.page.get_by_role("button", name="Create Event")
        self.url_input = self.page.locator("#url")  # Assuming the input field has an ID of 'url'
        self.title_input = self.page.locator("#title")  # Assuming the input field has an ID of 'title'
        self.date_time_input = self.page.locator("#dateTime")  # Assuming the input field has an ID of 'dateTime'
        self.location_input = self.page.locator("#location")  # Assuming the input field has an ID of 'location'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")

    def create_user_event(self, user_data: dict):
        """Create an event with the given details."""
        self.create_event_button.click()
        self.url_input.fill(user_data["url"])
        self.title_input.fill(user_data["title"])
        self.date_time_input.fill(user_data["date_time"])
        self.location_input.fill(user_data["location"])
        self.submit_button.click()
        self.events_management_link.click()  # Return to the main page after creating the event