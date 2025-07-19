import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_base_url():
    """Return the BASE_URL from the environment (.env file)."""
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise RuntimeError("BASE_URL is not set in the environment or .env file.")
    return base_url

# Configure pytest-playwright settings from environment variables
def pytest_configure(config):
    """Configure pytest-playwright settings from environment variables."""
    # Set playwright settings based on .env values
    if os.getenv("HEADLESS"):
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        config.option.playwright_headed = not headless
        print(f"🔧 Set playwright_headed to: {not headless}")
    
    slow_mo_raw = os.getenv("SLOW_MO")
    if slow_mo_raw is not None:
        try:
            slow_mo = int(slow_mo_raw)
            print(f"🔍 Raw SLOW_MO from .env: {slow_mo_raw}")
            print(f"🔍 Parsed slow_mo value: {slow_mo}")
            config.option.playwright_slow_mo = slow_mo
            print(f"🔧 Set playwright_slow_mo to: {slow_mo}ms")
        except ValueError:
            print(f"⚠️  Invalid SLOW_MO value '{slow_mo_raw}', ignoring")
    else:
        print("⚠️  No SLOW_MO found in environment variables")

# Override pytest-playwright fixtures to use our configuration
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch with headless and slow_mo from environment."""
    # Configure headless setting
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    browser_type_launch_args["headless"] = headless
    print(f"🔧 Set browser headless to: {headless}")
    
    # Configure slow_mo setting
    slow_mo_raw = os.getenv("SLOW_MO", "50")
    print(f"🔍 Fixture: Raw SLOW_MO from .env: {slow_mo_raw}")
    try:
        slow_mo = int(slow_mo_raw) if slow_mo_raw else 50
        print(f"🔍 Fixture: Parsed slow_mo value: {slow_mo}")
        if slow_mo > 0:
            browser_type_launch_args["slow_mo"] = slow_mo
            print(f"🔧 Set browser launch slow_mo to: {slow_mo}ms")
        else:
            print("⚠️  Fixture: No SLOW_MO value or it's 0")
    except ValueError:
        print(f"⚠️  Fixture: Invalid SLOW_MO value '{slow_mo_raw}', using 50")
        slow_mo = 50
    
    return browser_type_launch_args 