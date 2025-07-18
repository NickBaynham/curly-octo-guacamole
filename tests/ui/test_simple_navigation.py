from playwright.sync_api import Page
import pytest

def test_simple_navigation(page: Page, base_url: str):
    """Test simple navigation using Playwright."""
    
    # Navigate to the base URL
    page.goto(base_url)
    
    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")
    
    # Check if the title is correct
    assert page.title() == "Events Management"
    
    # Click on a link to navigate to another page
    accounts_button = page.get_by_role("button", name="Manage Accounts")
    accounts_button.click()
    
    # Wait for the new page to load
    page.wait_for_load_state("networkidle")
    
    # Verify the new URL
    assert page.url == base_url + "/entity/Account"
    
    # Verify the title of the new page
    page_title = page.get_by_text("Accounts")
    assert page_title.is_visible(), "Accounts page title is not visible"

@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the application."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv("BASE_URL", "http://localhost:4200")

# pdm run pytest tests/ui/test_simple_navigation.py --log-cli-level=INFO --headed --slomo=500
# Configuration is set in pytest.ini - but is overridden by .env is present
