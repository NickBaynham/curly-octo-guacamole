import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv


class Controller:
    """Controller class for managing browser and page setup."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.base_url = None
        
        # Load environment variables
        self._load_env()
    
    def _load_env(self):
        """Load environment variables from .env file."""
        # Look for .env file in project root (current working directory)
        env_file = Path.cwd() / ".env"
        
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Loaded .env file from: {env_file}")
        else:
            print(f"⚠️  No .env file found at: {env_file}, using default values")
    
    def get_base_url(self) -> str:
        """Get the base URL from environment variables."""
        return os.getenv("BASE_URL", "http://localhost:4200")
    
    def setup(self) -> Page:
        """
        Setup browser and page for testing using environment variables.
        
        Returns:
            Page: Configured page object
        """
        # Get configuration from environment variables
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        slow_mo = int(os.getenv("SLOW_MO", "5000"))
        self.base_url = self.get_base_url()
        
        print(f"🔧 Browser config: headless={headless}, slow_mo={slow_mo}ms")
        print(f"🌐 Base URL: {self.base_url}")
        
        # Setup browser and page
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
        self.page = self.browser.new_page()
        
        # Navigate to base URL
        self.page.goto(self.base_url)
        
        return self.page
    
    def cleanup(self):
        """Clean up browser and playwright resources."""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop() 