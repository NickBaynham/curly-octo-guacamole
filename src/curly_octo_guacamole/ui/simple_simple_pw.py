from playwright.sync_api import sync_playwright

def wait_for_angular_ready(page, timeout=10000):
    """Wait for Angular to be ready and all requests to complete."""
    try:
        # Wait for network to be idle
        page.wait_for_load_state("networkidle", timeout=timeout)
        
        # Wait for Angular to be ready (if Angular is present)
        page.wait_for_function("""
            () => {
                // Check if Angular is loaded
                if (!window.angular) return true;
                
                // Check if Angular is ready
                const body = document.body;
                const scope = window.angular.element(body).scope();
                if (!scope) return true;
                
                // Check if digest cycle is complete
                if (scope.$$phase) return false;
                
                // Check if HTTP requests are pending
                if (scope.$http && scope.$http.pendingRequests.length > 0) return false;
                
                return true;
            }
        """, timeout=timeout)
        
        print("✅ Angular is ready")
        return True
        
    except Exception as e:
        print(f"⚠️  Angular wait timeout: {e}")
        return False

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=5000)
page = browser.new_page()
base_url = "http://localhost:4200"
page.goto(base_url)

# Wait for page to be ready
page.wait_for_load_state("networkidle")
# Wait for Angular to be ready before clicking
wait_for_angular_ready(page)

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
    button = error_notification.locator("button.close-button")
    button.click()
page.close()
browser.close()
