import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.curly_octo_guacamole.ui.framework.waits import Waits
from src.curly_octo_guacamole.ui.framework.controller import Controller

# Setup browser and page
controller = Controller()
page = controller.setup()

base_url = controller.get_base_url()

# Wait for page to be ready
page.wait_for_load_state("networkidle")
# Wait for Angular to be ready before clicking
Waits.wait_for_angular_ready(page)

button = page.get_by_role("button", name="Manage Users")
button.click()
current_url = page.url
print(f"Current URL after navigation: {current_url}")

# Check for error notifications
error_notification = page.locator("div.notification-container.error")
error_exists = error_notification.count() > 0
print("Error on page?", error_exists)
if error_exists:
    error_text = error_notification.text_content()
    print(f"Error message: {error_text}")
    close_button = error_notification.locator("button.close-button")
    close_button.click()

# Cleanup
controller.cleanup()
