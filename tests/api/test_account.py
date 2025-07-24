from playwright.sync_api import Playwright, expect
from datetime import datetime
import pytest



def test_fetch_account_list(playwright: Playwright) -> None:
    # Create a new APIRequestContext
    request_context = playwright.request.new_context()

    # Perform the GET
    response = request_context.get("http://localhost:5500/api/account")
    expect(response).to_be_ok()  # 2xx

    # Deserialize JSON
    payload = response.json()
    assert isinstance(payload, dict), f"Expected dict, got {type(payload)}"
    assert "data" in payload, "Response JSON must have a 'data' key"

    data = payload["data"]
    assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    assert len(data) > 0, "Expected at least one account in the list"

    # Validate each entry
    for idx, item in enumerate(data):
        assert isinstance(item, dict), f"Item #{idx} is not a dict"
        # Required keys
        for key in ("id", "expiredAt", "createdAt", "updatedAt"):
            assert key in item, f"Missing '{key}' in item #{idx}"

        # id must be a string
        assert isinstance(item["id"], str), f"id must be str in item #{idx}"

        # expiredAt can be null or ISO string
        exp = item["expiredAt"]
        assert exp is None or isinstance(exp, str), f"expiredAt invalid in item #{idx}"

        # createdAt / updatedAt must be ISO timestamp strings
        for ts_key in ("createdAt", "updatedAt"):
            ts_val = item[ts_key]
            assert isinstance(ts_val, str), f"{ts_key} must be str in item #{idx}"
            # verify ISO format
            try:
                datetime.fromisoformat(ts_val)
            except ValueError:
                pytest.fail(f"{ts_key} in item #{idx} is not valid ISO datetime: {ts_val}")

    # Clean up
    request_context.dispose()

@pytest.mark.parametrize("account_id", [
    "687139d80e46574d4becf42c",
    # add more account IDs here as needed
])
def test_get_account_by_id(playwright: Playwright, account_id: str) -> None:
    # Arrange
    ctx = playwright.request.new_context()

    # Act
    url = f"http://localhost:5500/api/account/{account_id}"
    response = ctx.get(url)
    expect(response).to_be_ok()

    payload = response.json()

    # Assert top‐level structure
    assert isinstance(payload, dict), f"Expected JSON object, got {type(payload)}"
    for key in ("data", "message", "level", "metadata", "notifications", "status", "summary"):
        assert key in payload, f"Missing top‐level key: {key}"

    # Assert status and nullable fields
    assert payload["status"] == "perfect"
    assert payload["message"]       is None
    assert payload["level"]         is None
    assert payload["metadata"]      is None
    assert payload["notifications"] is None
    assert payload["summary"]       is None

    # Assert data array
    data = payload["data"]
    assert isinstance(data, list), f"'data' should be a list, got {type(data)}"
    assert len(data) == 1, f"Expected exactly one account, got {len(data)}"

    # Assert fields of the single account object
    account = data[0]
    for field in ("id", "expiredAt", "createdAt", "updatedAt"):
        assert field in account, f"Missing '{field}' in account object"

    assert account["id"] == account_id
    # expiredAt may be null or ISO string
    exp = account["expiredAt"]
    assert exp is None or isinstance(exp, str), f"expiredAt must be None or str, got {type(exp)}"

    # createdAt / updatedAt must parse as ISO datetimes
    for ts_key in ("createdAt", "updatedAt"):
        ts = account[ts_key]
        assert isinstance(ts, str), f"{ts_key} should be a string"
        try:
            # Python 3.11+ supports 6-digit microseconds
            datetime.fromisoformat(ts)
        except Exception:
            pytest.fail(f"{ts_key} is not valid ISO datetime: {ts}")

    # Cleanup
    ctx.dispose()    