"""Tests for authentication / session management."""
import os


def test_session_has_cookies(pinterest):
    """After login the session should have at least a csrftoken cookie."""
    cookies = pinterest.http.cookies.get_dict()
    assert len(cookies) > 0, "Expected cookies after login"


def test_cookies_persisted_to_disk(pinterest):
    """Registry should have written a cookie file to disk."""
    cred_path = os.path.join("data", os.environ["PINTEREST_EMAIL"])
    assert os.path.exists(cred_path), f"Cookie file not found at {cred_path}"
