"""Test for logout.

This runs LAST (via the zzz prefix in the class name) since it invalidates the session.
We skip it by default to avoid breaking other tests in the same run.
Run explicitly with: pytest tests/test_logout.py -v
"""
import pytest


@pytest.mark.skip(reason="Logout invalidates session - run manually with: pytest tests/test_logout.py -v --override-ini='addopts='")
def test_logout(pinterest):
    """Logout should return 200. WARNING: this invalidates the session cookies."""
    resp = pinterest.logout()
    assert resp.status_code == 200
