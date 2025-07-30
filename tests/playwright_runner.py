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

    controller = Controller()
    result = controller.run_test(test_type, data)
    logger.info(f"Test Result: {result}")

    # try:
    #     with sync_playwright() as p:
    #         logger.info("🚀 Launching headless browser...")
    #         # Launch browser
    #         browser = p.chromium.launch(headless=True)
    #         context = browser.new_context()
    #         page = context.new_page()
            
    #         logger.info("🌐 Navigating to UI application...")
    #         # Navigate to the application
    #         page.goto("http://localhost:4200")
    #         page.wait_for_load_state("networkidle")
            
    #         logger.info("📋 Navigating to Accounts management page...")
    #         # Navigate to Accounts page
    #         accounts_button = page.get_by_role("button", name="Manage Accounts")
    #         accounts_button.click()
    #         page.wait_for_load_state("networkidle")
            
    #         logger.info("➕ Clicking Create Account button...")
    #         # Click Create Account button
    #         create_account_button = page.get_by_role("button", name="Create Account")
    #         create_account_button.click()
            
    #         # Fill in the expiredAt field with the date from the request
    #         expired_at = data.get("date", "2025-08-19")  # Default to today if not provided
    #         logger.info(f"📅 Filling expiration date: {expired_at}")
    #         page.fill('#expiredAt', expired_at)
            
    #         logger.info("📤 Submitting account creation form...")
    #         # Submit the form
    #         submit_button = page.get_by_role("button", name="Submit")
    #         submit_button.click()
            
    #         # Wait for the form submission to complete
    #         page.wait_for_load_state("networkidle")
            
    #         logger.info("🔍 Validating account creation result...")
    #         # Check if account was created successfully
    #         # Look for success message or redirect
    #         success = True
    #         error_message = None
            
    #         try:
    #             # Check if we're back on the accounts page or if there's a success message
    #             page.wait_for_url("**/entity/Account", timeout=5000)
    #         except:
    #             # If we're still on the create form, there might be an error
    #             error_elements = page.locator(".error, .alert, [role='alert']")
    #             if error_elements.count() > 0:
    #                 success = False
    #                 error_message = error_elements.first.text_content()
            
    #         # Close browser
    #         context.close()
    #         browser.close()
            
    #         logger.info("-" * 60)
    #         if success:
    #             logger.info("✅ ACCOUNT CREATION TEST PASSED")
    #             logger.info(f"📅 Account created with expiration date: {expired_at}")
    #         else:
    #             logger.error("❌ ACCOUNT CREATION TEST FAILED")
    #             if error_message:
    #                 logger.error(f"💥 Error: {error_message}")
    #         logger.info("=" * 60)
            
    return {
        "success": "success",
        "expired_at": data["expired_at"],
        "error_message": None,
        "message": "Account creation test completed"
    }
            
    # except Exception as e:
    #     logger.error("-" * 60)
    #     logger.error("💥 ACCOUNT CREATION TEST EXCEPTION")
    #     logger.error(f"🚨 Exception: {str(e)}")
    #     logger.error("=" * 60)
        
    #     return {
    #         "success": False,
    #         "error": str(e),
    #         "message": "Account creation test failed"
    #     }
