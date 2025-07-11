import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = Path.cwd() / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded .env file from: {env_file}")
else:
    print(f"⚠️  No .env file found at: {env_file}")

# Configure pytest-playwright settings from environment variables
def pytest_configure(config):
    """Configure pytest-playwright settings from environment variables."""
    # Set playwright settings based on .env values
    if os.getenv("HEADLESS"):
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        config.option.playwright_headed = not headless
        print(f"🔧 Set playwright_headed to: {not headless}")
    
    if os.getenv("SLOW_MO"):
        slow_mo = int(os.getenv("SLOW_MO", "0"))
        print(f"🔍 Raw SLOW_MO from .env: {os.getenv('SLOW_MO')}")
        print(f"🔍 Parsed slow_mo value: {slow_mo}")
        config.option.playwright_slow_mo = slow_mo
        print(f"🔧 Set playwright_slow_mo to: {slow_mo}ms")
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
    slow_mo = int(os.getenv("SLOW_MO", "0"))
    print(f"🔍 Fixture: Raw SLOW_MO from .env: {os.getenv('SLOW_MO')}")
    print(f"🔍 Fixture: Parsed slow_mo value: {slow_mo}")
    if slow_mo > 0:
        browser_type_launch_args["slow_mo"] = slow_mo
        print(f"🔧 Set browser launch slow_mo to: {slow_mo}ms")
    else:
        print("⚠️  Fixture: No SLOW_MO value or it's 0")
    
    return browser_type_launch_args 