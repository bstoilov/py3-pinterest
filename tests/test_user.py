"""Tests for user-related API calls."""
import os

PINTEREST_USERNAME = os.environ.get("PINTEREST_USERNAME", "ccocoho")


def test_get_user_overview(pinterest):
    result = pinterest.get_user_overview(username=PINTEREST_USERNAME)
    assert result is not None
    assert "username" in result
    assert result["username"] == PINTEREST_USERNAME


def test_get_user_overview_self(pinterest):
    """When no username is given it should default to the current user."""
    result = pinterest.get_user_overview()
    assert result is not None
    assert "username" in result


def test_get_user_pins(pinterest):
    result = pinterest.get_user_pins(username=PINTEREST_USERNAME, reset_bookmark=True)
    assert isinstance(result, list)


def test_get_following(pinterest):
    result = pinterest.get_following(username=PINTEREST_USERNAME, reset_bookmark=True)
    assert isinstance(result, list)


def test_get_following_all(pinterest):
    result = pinterest.get_following_all(username=PINTEREST_USERNAME)
    assert isinstance(result, list)


def test_get_user_followers(pinterest):
    result = pinterest.get_user_followers(username=PINTEREST_USERNAME, reset_bookmark=True)
    assert isinstance(result, list)


def test_get_user_followers_all(pinterest):
    result = pinterest.get_user_followers_all(username=PINTEREST_USERNAME)
    assert isinstance(result, list)
