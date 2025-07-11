from playwright.sync_api import Page


class Waits:
    """Utility class for waiting for various page states and conditions."""
    
    @staticmethod
    def wait_for_angular_ready(page: Page, timeout: int = 10000) -> bool:
        """
        Wait for Angular to be ready and all requests to complete.
        
        Args:
            page: Playwright page object
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            bool: True if Angular is ready, False if timeout occurred
        """
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
    
    @staticmethod
    def wait_for_page_ready(page: Page, timeout: int = 10000) -> bool:
        """
        Wait for page to be fully loaded and ready.
        
        Args:
            page: Playwright page object
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            bool: True if page is ready, False if timeout occurred
        """
        try:
            # Wait for DOM to be ready
            page.wait_for_load_state("domcontentloaded")
            
            # Wait for network to be idle
            page.wait_for_load_state("networkidle")
            
            # Wait for Angular to be ready
            page.wait_for_function("""
                () => {
                    if (!window.angular) return true;
                    const scope = window.angular.element(document.body).scope();
                    return !scope || (!scope.$$phase && (!scope.$http || scope.$http.pendingRequests.length === 0));
                }
            """, timeout=timeout)
            
            # Wait for any loading indicators to disappear
            try:
                page.wait_for_selector(".loading, .spinner, [data-loading]", state="hidden", timeout=5000)
            except:
                pass  # No loading indicators found
                
            print("✅ Page is ready")
            return True
            
        except Exception as e:
            print(f"⚠️  Page wait timeout: {e}")
            return False 