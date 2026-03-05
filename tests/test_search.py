"""Tests for search and type-ahead."""


def test_search_pins(pinterest):
    results = pinterest.search(scope="pins", query="python programming", page_size=10, reset_bookmark=True)
    assert isinstance(results, list)
    assert len(results) > 0


def test_search_boards(pinterest):
    results = pinterest.search(scope="boards", query="recipes", page_size=10, reset_bookmark=True)
    assert isinstance(results, list)


def test_type_ahead(pinterest):
    results = pinterest.type_ahead(term="python")
    assert isinstance(results, list)
    assert len(results) > 0
