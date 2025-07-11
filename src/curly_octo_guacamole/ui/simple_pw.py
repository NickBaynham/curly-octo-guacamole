# Here I'm creating a simple Python Test Script
from playwright.sync_api import sync_playwright

def navigate_to_entity(page, entity_name):
    """Navigate to root URL and click on the specified entity button, then return the URL."""
    page.goto(root_url)
    button = page.get_by_role("button", name=entity_name)
    button.click()
    url = page.url
    print(f"{entity_name}:", url)

    # Check for error notifications
    notif = page.locator("div.notification-container.error")
    
    # Option 1: Check if error is immediately visible
    visible = notif.is_visible()
    print("error visible?", visible)
    
    # Option 2: Wait for error to appear (with timeout)
    try:
        notif.wait_for(state="visible", timeout=5000)
        print("Error notification appeared!")
        # Get error message if needed
        error_text = notif.text_content()
        print(f"Error message: {error_text}")
    except:
        print("No error notification appeared within timeout")
    
    # Option 3: Check for success (no error)
    if not visible:
        print(f"Successfully navigated to {entity_name}")
    else:
        print(f"Error navigating to {entity_name}")

    # Check if the URL has changed
    return url

root_url = 'http://localhost:4200'
print('Testing ', root_url)

# List of entity names to test
entity_names = [
    "Manage Accounts",
    "Manage Users", 
    "Manage User Profiles",
    "Manage Event Affinity",
    "Manage Events",
    "Manage Event Attendance",
    "Manage URLs",
    "Manage Crawls"
]

with sync_playwright() as playwright:
    print("Playwright Started.")
    # Launch a Browser
    # browser = playwright.chromium.launch(headless=False, slow_mo=500)
    browser = playwright.chromium.launch()
    # Create a new Page
    page = browser.new_page()

    # Test navigation for each entity
    for entity_name in entity_names:
        navigate_to_entity(page, entity_name)

    # Close the Browser
    browser.close()
print("Who doesn't love Guacamole? Test Completed.")