# tests/playwright_runner.py
from playwright.sync_api import sync_playwright
import subprocess
import json
import sys
import logging
from pathlib import Path

from curly_octo_guacamole.api.controllers.controller import Controller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_test(keyword: str, data: dict) -> dict:
    """
    Dispatch to your Playwright test modules based on `keyword`.
    For demo, we'll just echo back.
    """
    # Example: if keyword == "create_account", run a Python module or subprocess
    # result = subprocess.run(["pytest", f"--keyword={keyword}", f"--data={json.dumps(data)}"], capture_output=True)
    # return {"stdout": result.stdout.decode(), "returncode": result.returncode}
    
    if keyword == "create_account":
        return run_create_account_test(data)
    elif keyword == "create_user":
        return run_create_user_test(data)
    
    return {"keyword": keyword, "received": data}

def run_create_account_test(data: dict) -> dict:
    """
    Run the account creation test using Playwright.
    """
    logger.info("=" * 60)
    logger.info("🧪 ACCOUNT CREATION TEST STARTED")
    logger.info("=" * 60)
    logger.info(f"📋 Test Description: Creating account with expiration date from the request data")
    logger.info(f"📅 Request Data: {data}")
    logger.info(f"🎯 Target UI: http://localhost:4200")
    logger.info(f"🔧 Test Type: Playwright UI Automation")
    logger.info("-" * 60)

    if data["ui_test"]:
        test_type = "ui"
    else:
        test_type = "api"

    # Add test_type to data for controller routing
    data["test_type"] = "account"

    controller = Controller()
    result = controller.run_test(test_type, data)
    logger.info(f"Test Result: {result}")

    # Return the actual controller result instead of hardcoded response
    return result

def run_create_user_test(data: dict) -> dict:
    """
    Run the user creation test using Playwright.
    """
    logger.info("=" * 60)
    logger.info("🧪 USER CREATION TEST STARTED")
    logger.info("=" * 60)
    logger.info(f"📋 Test Description: Creating user with data from the request")
    logger.info(f"📅 Request Data: {data}")
    logger.info(f"🎯 Target UI: http://localhost:4200")
    logger.info(f"🔧 Test Type: Playwright UI Automation")
    logger.info("-" * 60)

    if data["ui_test"]:
        test_type = "ui"
    else:
        test_type = "api"

    # Add test_type to data for controller routing
    data["test_type"] = "user"

    controller = Controller()
    result = controller.run_test(test_type, data)
    logger.info(f"Test Result: {result}")

    # Return the actual controller result instead of hardcoded response
    return result
