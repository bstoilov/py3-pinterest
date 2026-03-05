"""Tests for comment-related API calls."""
import pytest


@pytest.fixture(scope="module")
def pin_with_comments(pinterest):
    """Find a pin via search that we can try to read comments from."""
    results = pinterest.search(scope="pins", query="funny cats", page_size=10, reset_bookmark=True)
    assert len(results) > 0
    return results[0]["id"]


def test_get_comments(pinterest, pin_with_comments):
    comments = pinterest.get_comments(pin_id=pin_with_comments, reset_bookmark=True)
    assert isinstance(comments, list)
