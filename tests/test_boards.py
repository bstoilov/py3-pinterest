"""Tests for board-related API calls."""
import os
import uuid
import pytest

PINTEREST_USERNAME = os.environ.get("PINTEREST_USERNAME", "ccocoho")


def test_boards_list(pinterest):
    result = pinterest.boards(username=PINTEREST_USERNAME, reset_bookmark=True)
    assert isinstance(result, list)


def test_boards_all(pinterest):
    result = pinterest.boards_all(username=PINTEREST_USERNAME)
    assert isinstance(result, list)


def test_create_and_delete_board(pinterest):
    board_name = f"test_{uuid.uuid4().hex[:8]}"
    resp = pinterest.create_board(name=board_name, description="Auto-generated integration test board")
    data = resp.json()
    assert "resource_response" in data
    board = data["resource_response"]["data"]
    assert board["name"] == board_name
    assert "id" in board

    # Cleanup
    pinterest.delete_board(board_id=board["id"])


def test_board_feed(pinterest, test_board):
    result = pinterest.board_feed(board_id=test_board["id"], reset_bookmark=True)
    assert isinstance(result, list)


def test_board_sections_empty(pinterest, test_board):
    result = pinterest.get_board_sections(board_id=test_board["id"], reset_bookmark=True)
    assert isinstance(result, list)


def test_create_and_delete_board_section(pinterest, test_board):
    resp = pinterest.create_board_section(
        board_id=test_board["id"], section_name="test_section"
    )
    section = resp.json()["resource_response"]["data"]
    assert section["title"] == "test_section"

    # Delete section
    pinterest.delete_board_section(section_id=section["id"])


def test_section_pins(pinterest, test_board):
    """Create a section, pin into it, read section pins, then clean up."""
    # Create section
    resp = pinterest.create_board_section(
        board_id=test_board["id"], section_name="pins_section"
    )
    section = resp.json()["resource_response"]["data"]
    section_id = section["id"]

    # Pin into the section
    resp = pinterest.pin(
        board_id=test_board["id"],
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png",
        description="Section pin test",
        title="Section Test",
        section_id=section_id,
    )
    pin = resp.json()["resource_response"]["data"]

    # Read section pins
    result = pinterest.get_section_pins(section_id=section_id, reset_bookmark=True)
    assert isinstance(result, list)

    # Cleanup
    pinterest.delete_pin(pin_id=pin["id"])
    pinterest.delete_board_section(section_id=section_id)


def test_board_recommendations(pinterest, test_board):
    result = pinterest.board_recommendations(board_id=test_board["id"], reset_bookmark=True)
    assert isinstance(result, list)


def test_board_invites(pinterest, test_board):
    result = pinterest.get_board_invites(board_id=test_board["id"])
    assert isinstance(result, list)


def test_board_invites_all(pinterest, test_board):
    result = pinterest.get_board_invites_all(board_id=test_board["id"])
    assert isinstance(result, list)
