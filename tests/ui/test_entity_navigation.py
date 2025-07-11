import pytest
from playwright.sync_api import Page, expect

def test_entity_navigation(page: Page):
    """Test navigation to all entity management pages."""
    root_url = 'http://localhost:4200'
    
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
        button = page.get_by_role("button", name=entity_name)
        button.click()
        current_url = page.url
        assert current_url != root_url, f"Navigation failed for {entity_name} - URL did not change"

        # Check for any element with 'error' in its class or text
        error_elements = page.locator("*")
        error_count = error_elements.count()
        found_error = False
        error_details = []
        for i in range(error_count):
            el = error_elements.nth(i)
            class_attr = el.get_attribute("class") or ""
            text = el.text_content() or ""
            if "error" in class_attr.lower() or "error" in text.lower():
                found_error = True
                error_details.append(f"Element {i+1}: class='{class_attr}', text='{text[:100]}...'")
                # Try to close the error if possible
                try:
                    close_button = el.locator("button")
                    if close_button.count() > 0:
                        close_button.click()
                except Exception:
                    pass
        # Also check for 'error' in the page body text
        body_text = page.locator("body").text_content() or ""
        if "error" in body_text.lower():
            found_error = True
            error_details.append(f"'error' found in page body text: ...{body_text.lower().find('error')}")
        if found_error:
            print(f"❌ Error detected for {entity_name}:")
            for detail in error_details:
                print(detail)
            assert False, f"Error detected for {entity_name}"
        else:
            print(f"✅ No error detected for {entity_name}")
        print(f"{entity_name}: {current_url}")


def test_entity_buttons_exist(page: Page):
    """Test that all entity management buttons are present on the main page."""
    root_url = 'http://localhost:4200'
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