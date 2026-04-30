import os
import pytest
from dotenv import load_dotenv
from py3pin.Pinterest import Pinterest

load_dotenv()

PINTEREST_EMAIL = os.environ["PINTEREST_EMAIL"]
PINTEREST_PASSWORD = os.environ["PINTEREST_PASSWORD"]
PINTEREST_USERNAME = os.environ["PINTEREST_USERNAME"]

TEST_BOARD_NAME = "test"


@pytest.fixture(scope="session")
def pinterest():
    """
    Session-scoped Pinterest client.
    Login is only triggered if there are no cached cookies (i.e. first run ever
    or cookies expired). After login, cookies are persisted to disk by the
    Registry so subsequent test runs reuse them without hitting login again.
    """
    client = Pinterest(
        email=PINTEREST_EMAIL,
        password=PINTEREST_PASSWORD,
        username=PINTEREST_USERNAME,
        cred_root="data",
    )

    # Only login if we don't already have a valid session.
    # We check by trying a lightweight call; if it fails we login once.
    if not _has_valid_session(client):
        print("\n[conftest] No valid session found, logging in via Selenium...")
        client.login()
    else:
        print("\n[conftest] Reusing existing session cookies.")

    return client


@pytest.fixture(scope="session")
def test_board(pinterest):
    """
    Session-scoped board named 'test'.
    Looks for an existing board with that name; creates one if missing.
    The board is NOT deleted after tests so it can be reused across runs.
    """
    boards = pinterest.boards(username=PINTEREST_USERNAME, page_size=250, reset_bookmark=True)
    for b in boards:
        if b.get("name") == TEST_BOARD_NAME:
            return b

    resp = pinterest.create_board(name=TEST_BOARD_NAME)
    return resp.json()["resource_response"]["data"]


def _has_valid_session(client):
    """Check if current cookies give us a valid session."""
    try:
        result = client.get_user_overview(username=PINTEREST_USERNAME)
        return result is not None and "username" in result
    except Exception:
        return False
