"""Tests for pin-related API calls."""
import pytest


@pytest.fixture(scope="module")
def sample_pin_id(pinterest):
    """Get a pin ID from search results to use in tests."""
    results = pinterest.search(scope="pins", query="landscape photography", page_size=5, reset_bookmark=True)
    assert len(results) > 0
    return results[0]["id"]


def test_load_pin(pinterest, sample_pin_id):
    pin_data = pinterest.load_pin(pin_id=sample_pin_id)
    assert pin_data is not None
    assert "id" in pin_data


def test_get_pinnable_images(pinterest):
    urls = pinterest.get_pinnable_images(url="https://en.wikipedia.org/wiki/Python_(programming_language)")
    assert isinstance(urls, list)


def test_home_feed(pinterest):
    result = pinterest.home_feed(page_size=10, reset_bookmark=True)
    assert isinstance(result, list)


def test_visual_search(pinterest, sample_pin_id):
    """Visual search using a pin's image."""
    pin_data = pinterest.load_pin(pin_id=sample_pin_id)
    # visual_search needs images.orig with width/height and image_signature
    if "images" not in pin_data or "orig" not in pin_data.get("images", {}):
        pytest.skip("Pin does not have images.orig data needed for visual search")
    if "image_signature" not in pin_data:
        pytest.skip("Pin does not have image_signature needed for visual search")

    results = pinterest.visual_search(pin_data=pin_data, reset_bookmark=True)
    assert isinstance(results, list)
