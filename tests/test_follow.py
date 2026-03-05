"""Tests for follow/unfollow actions.

We follow and immediately unfollow to avoid leaving side-effects.
"""
import pytest


@pytest.fixture(scope="module")
def target_user_id(pinterest):
    """Find a user to follow/unfollow via search."""
    results = pinterest.search(scope="pins", query="photography", page_size=5, reset_bookmark=True)
    for r in results:
        if "pinner" in r and "id" in r["pinner"]:
            return r["pinner"]["id"]
    pytest.skip("Could not find a user to follow in search results")


def test_follow_and_unfollow_user(pinterest, target_user_id):
    resp = pinterest.follow_user(user_id=target_user_id)
    assert resp.status_code == 200

    resp = pinterest.unfollow_user(user_id=target_user_id)
    assert resp.status_code == 200


@pytest.fixture(scope="module")
def target_board_id(pinterest):
    """Find a board to follow/unfollow via search."""
    results = pinterest.search(scope="boards", query="travel", page_size=5, reset_bookmark=True)
    for r in results:
        if "id" in r:
            return r["id"]
    pytest.skip("Could not find a board to follow in search results")


def test_follow_and_unfollow_board(pinterest, target_board_id):
    resp = pinterest.follow_board(board_id=target_board_id)
    assert resp.status_code == 200

    resp = pinterest.unfollow_board(board_id=target_board_id)
    assert resp.status_code == 200
