import logging
from playwright.sync_api import Page
from tests.conftest import get_base_url

class UserEventPage:
    def __init__(self, page: Page):
        self.page = page
        self.attendance_button = self.page.get_by_role("button", name="Manage Event Attendance")
        self.create_user_event_button = page.get_by_role("button", name="Create UserEvent")
        self.url_input = self.page.locator("#url")  # Assuming the input field has an ID of 'url'
        self.title_input = self.page.locator("#title")  # Assuming the input field has an ID of 'title'
        self.date_time_input = self.page.locator("#dateTime")  # Assuming the input field has an ID of 'dateTime'
        self.location_input = self.page.locator("#location")  # Assuming the input field has an ID of 'location'
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.events_management_link = self.page.get_by_text("Events Management")
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def create_user_event(self, user_data: dict):
        """Create an event with the given details."""

        self.page.goto(get_base_url())
        self.attendance_button.click()
        self.create_user_event_button.click()

        # Fill in the user event attended value
        if user_data["attended"]:
            self.page.check('#attended')
        else:
            self.page.uncheck('#attended')

        self.page.fill('input[type="number"]', str(user_data["rating"]))
        self.page.fill('#eventId', user_data["event_id"])
        self.page.fill('#userId', user_data["user_id"])
        self.log.info("Filled user details: %s", user_data)

        # Click the "Submit" button to submit the form
        self.submit_button.click()
        self.log.info("Clicked 'Submit' button to create user event")

        # Click the "Events Management" link to return home
        self.events_management_link.click()
