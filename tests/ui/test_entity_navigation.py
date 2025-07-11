import pytest
from playwright.sync_api import Page, expect
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from curly_octo_guacamole.ui.framework.waits import Waits
from curly_octo_guacamole.ui.framework.assertions import SoftAssert

def test_entity_navigation(page: Page):
    """Test navigation to all entity management pages."""
    # Get base URL from environment (without creating browser instance)
    import os
    from dotenv import load_dotenv
    load_dotenv()
    root_url = os.getenv("BASE_URL", "http://localhost:4200")
    
    # Create soft assert instance
    soft_assert = SoftAssert()
    
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
    
    for entity_name in entity_names:
        page.goto(root_url)
        
        # Wait for Angular to be ready before clicking
        Waits.wait_for_angular_ready(page)
        
        button = page.get_by_role("button", name=entity_name)
        button.click()
        
        # Wait for navigation to complete and Angular to be ready again
        Waits.wait_for_angular_ready(page)
        
        current_url = page.url
        soft_assert.assert_not_equal(current_url, root_url, f"Navigation failed for {entity_name} - URL did not change")

        # Check for error notifications
        error_notification = page.locator("div.notification-container.error")
        error_exists = error_notification.count() > 0
        print("Error on page?", error_exists)
        if error_exists:
            error_text = error_notification.text_content()
            print(f"Error message: {error_text}")
            close_button = error_notification.locator("button.close-button")
            close_button.click()
        soft_assert.assert_false(error_exists, f"Error notification appeared for {entity_name}")
    
    # Check all soft assertions at the end
    soft_assert.assert_all()

def test_entity_buttons_exist(page: Page):
    """Test that all entity management buttons are present on the main page."""
    # Get base URL from environment (without creating browser instance)
    import os
    from dotenv import load_dotenv
    load_dotenv()
    root_url = os.getenv("BASE_URL", "http://localhost:4200")
    page.goto(root_url)
    
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
    
    for entity_name in entity_names:
        button = page.get_by_role("button", name=entity_name)
        expect(button).to_be_visible()
        print(f"✓ Button '{entity_name}' is present and visible")


def test_all_entity_functionality(page: Page):
    """Test all entity functionality by running both test functions."""
    # Test that all buttons exist first
    test_entity_buttons_exist(page)
    
    # Then test navigation to all entities
    test_entity_navigation(page)