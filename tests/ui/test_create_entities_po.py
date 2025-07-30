import logging
from playwright.sync_api import Page
import pytest
import sys
from pathlib import Path

from tests.conftest import get_base_url
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
import curly_octo_guacamole.ui.framework.utils as utils

from curly_octo_guacamole.ui.framework.page_objects.account_page import AccountPage
from curly_octo_guacamole.ui.framework.page_objects.user_page import UserPage
from curly_octo_guacamole.ui.framework.page_objects.event_page import EventPage
from curly_octo_guacamole.ui.framework.page_objects.profile_page import ProfilePage
from curly_octo_guacamole.ui.framework.page_objects.affinity_page import AffinityPage
from curly_octo_guacamole.ui.framework.page_objects.user_event_page import UserEventPage
from datetime import datetime

def test_create_entities_po(page: Page, log: logging.Logger):
    """Test creating entities using the UI with Page Objects"""
    page.goto(get_base_url())
    page.wait_for_load_state("networkidle")
    assert page.title() == "Events Management"

    # Accounts
    account_page = AccountPage(page)
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = {
        "expired_at": today,
    }
    account_page.create_account(user_data)
    log.info("Created account with expiredAt: %s", today)

    # Users
    user_page = UserPage(page)
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "nobody@nowhere.com",
        "first_name": "Test",
        "last_name": "User",
        "gender": "female",
        "dob": "1990-01-01",
        "owner": False,
        "net_worth": 1000000,
        "account_id": "6871326a0e46574d4becf423",
    }
    user_page.create_user(user_data)
    log.info("Created user: %s", user_data)

    # Events
    event_page = EventPage(page)
    event_data = {
        "url": "https://url.com",
        "title": "this is a title",
        "date_time": "2025-01-01",
        "location": "444 Event Drive, Anytown, CA 90102",
    }
    event_page.create_event(event_data)
    log.info("Created event: %s", event_data)

    # Profiles
    profile_page = ProfilePage(page)
    profile_data = {
        "name": "profile 1",
        "user_id": "nobody@nowhere.com",
        "radius_miles": 100,
    }
    profile_page.create_profile(profile_data)
    log.info("Created profile: %s", profile_data)

    # Affinities
    affinity_page = AffinityPage(page)
    affinity_data = {
        "tag": "tag 1",
        "affinity": 1,
        "profile_id": "68713c4c0e46574d4becf437",
    }
    affinity_page.create_affinity(affinity_data)
    log.info("Created affinity: %s", affinity_data)

    # User Events
    user_event_page = UserEventPage(page)
    user_event_data = {
        "attended": True,
        "rating": 5,
        "event_id": "68713f650e46574d4becf43c",
        "user_id": "687133d20e46574d4becf424",
    }
    
    user_event_page.create_user_event(user_event_data)
    log.info("Created user event: %s", user_event_data)

@pytest.fixture(scope="session")
def log():
    logger = logging.getLogger("test_create_entities_po")
    logger.setLevel(logging.INFO)
    return logger
