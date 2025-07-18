import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

# from curly_octo_guacamole.ui.framework import Create


def test_create_scenario():
    # create = Create()

    # 1. Create an Account with future expiry date
    future_date = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    # create.create_account(expiration_date=future_date)

    # 2. Add a user to the Account that is the owner and an additional user
    account_id = 'account_id_placeholder'  # Replace with actual account id if available
    user1 = {
        'user_name': 'owneruser',
        'email': 'owner@example.com',
        'password': 'Password123!',
        'first_name': 'Owner',
        'last_name': 'User',
        'owner': True,
        'account': account_id
    }
    user2 = {
        'user_name': 'seconduser',
        'email': 'second@example.com',
        'password': 'Password123!',
        'first_name': 'Second',
        'last_name': 'User',
        'owner': False,
        'account': account_id
    }
    # create.create_user(**user1)
    # create.create_user(**user2)

    # 3. Create a profile for each user
    profile1 = {'name': 'OwnerProfile', 'user_id': 'user1_id_placeholder'}
    profile2 = {'name': 'SecondProfile', 'user_id': 'user2_id_placeholder'}
    # create.create_profile(**profile1)
    # create.create_profile(**profile2)

    # 4. Create a tag affinity for each user profile
    # create.create_tag_affinity(tag='sports', affinity=80, profile_id='profile1_id_placeholder')
    # create.create_tag_affinity(tag='music', affinity=60, profile_id='profile2_id_placeholder')

    # 5. Create two events
    event1 = {
        'url': 'https://event1.com',
        'title': 'Event One',
        'date_time': '2025-01-01T10:00:00',
        'location': 'Venue A'
    }
    event2 = {
        'url': 'https://event2.com',
        'title': 'Event Two',
        'date_time': '2025-02-01T15:00:00',
        'location': 'Venue B'
    }
    # create.create_event(**event1)
    # create.create_event(**event2)

    # 6. Assign an event to a user, and then both events to another user
    # create.create_user_event(user_id='user1_id_placeholder', event_id='event1_id_placeholder')
    # create.create_user_event(user_id='user2_id_placeholder', event_id='event1_id_placeholder')
    # create.create_user_event(user_id='user2_id_placeholder', event_id='event2_id_placeholder')

    # 7. Create one or more URLs
    # create.create_url(urls='https://resource.com', params={'type': 'resource'}) 

# pdm run pytest --version
