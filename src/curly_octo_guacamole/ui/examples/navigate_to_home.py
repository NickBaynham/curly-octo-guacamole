from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=5000)
page = browser.new_page()
page.goto("http://localhost:4200")

page.close()
browser.close()
playwright.stop()


# pdm run src/curly_octo_guacamole/ui/examples/example_2.py
# This script demonstrates how to use Playwright to launch a browser,
# navigate to a specific URL, and then close the browser.
# It uses the sync API for simplicity.
# The `sync_playwright` function is used to start Playwright,
# and the `chromium.launch` method is used to launch a Chromium browser instance.
# The `headless` option is set to True to run the browser in headless mode,
# and the `slow_mo` option is set to 5000 milliseconds to slow down interactions for debugging purposes.
# After navigating to the specified URL, the script closes the page and the browser.
# This is a basic example of using Playwright for browser automation.
# The script can be extended with more complex interactions,
# such as clicking buttons, filling forms, and verifying page content.
# Playwright's capabilities allow for comprehensive browser automation,
# making it suitable for end-to-end testing and web scraping tasks.
# The script can be run in a Python environment with Playwright installed.
# Ensure you have Playwright installed with `pip install playwright`
# and have the necessary browser binaries downloaded using `playwright install`.
# This script is a starting point for using Playwright in Python.
# You can build upon it to create more complex browser automation tasks.
# Playwright's API provides a rich set of features for interacting with web pages,
# handling events, and managing browser contexts.
# This script is a simple demonstration of how to use Playwright