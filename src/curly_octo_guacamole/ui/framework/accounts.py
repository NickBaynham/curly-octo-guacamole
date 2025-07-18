
import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from curly_octo_guacamole import Controller
from curly_octo_guacamole.ui.framework.waits import Waits
from curly_octo_guacamole.ui.framework.accounts import Accounts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Launch the browser using the controller class

controller = Controller()
page = controller.setup()
# Navigate to the base URL
base_url = controller.get_base_url()
# Wait for the page to load completely
page.wait_for_load_state("networkidle")
# Wait for Angular to be ready before clicking
Waits.wait_for_angular_ready(page)

# Click the "Manage Accounts" button

accounts_button = page.get_by_role("button", name="Manage Accounts")
accounts_button.click()
# Get the current URL after navigation
current_url = page.url
logger.info(f"Current URL after navigation: {current_url}")
# Check for error notifications
error_notification = page.locator("div.notification-container.error")
error_exists = error_notification.count() > 0
logger.info("Error on page? %s", error_exists)
if error_exists:
    error_text = error_notification.text_content()
    logger.error(f"Error message: {error_text}")
    # Close the error notification
    close_button = error_notification.locator("button.close-button")
    close_button.click()

# Create an instance of the Accounts class
accounts = Accounts(page)
# Click the "Manage Users" button
accounts.click_manage_users_button()
# Get the current URL after navigation
current_url = page.url
logger.info(f"Current URL after navigation: {current_url}")
# Check for error notifications
error_exists, error_text = accounts.check_for_error_notifications()
logger.info("Error on page? %s", error_exists)
if error_exists:
    logger.error(f"Error message: {error_text}")

# Verify the browser is on the     
    accounts.close_error_notification()
# Cleanup the controller
controller.cleanup()
# End of the script
# This script demonstrates how to use the Accounts class to manage user accounts
# and handle error notifications in a web application using Playwright.
# The Accounts class encapsulates the functionality related to user account management.
# It provides methods to click buttons, check for error notifications,
# and close error notifications.
# This modular approach makes the code cleaner and easier to maintain.
# The script also includes necessary imports and setup for Playwright,
# ensuring that the browser is launched and the page is ready for interaction.
# The Accounts class can be extended with more methods as needed
# for additional user account management functionalities.
# This script is a simple demonstration of how to use the Accounts class
# in a Playwright-based web automation context.
# The Accounts class can be further extended with more methods
# for additional user account management functionalities.
# The script is designed to be modular and reusable,