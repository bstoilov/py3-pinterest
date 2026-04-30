"""Tests for pin create / repin / delete / upload / comment / note actions.

These tests create real pins and then clean them up.
Uses the shared 'test_board' fixture from conftest.py.
"""
import os
import tempfile
import pytest


@pytest.fixture(scope="module")
def owned_pin(pinterest, test_board):
    """Create a pin we own for tests that need one."""
    resp = pinterest.pin(
        board_id=test_board["id"],
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png",
        description="Test pin for actions",
        title="Owned Test Pin",
    )
    pin = resp.json()["resource_response"]["data"]
    yield pin
    # Cleanup - delete pin if it still exists
    try:
        pinterest.delete_pin(pin_id=pin["id"])
    except Exception:
        pass


class TestPinActions:
    """Grouped so they share the test_board fixture and run together."""

    def test_pin_from_url(self, pinterest, test_board):
        resp = pinterest.pin(
            board_id=test_board["id"],
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png",
            description="Integration test pin",
            title="Test Pin",
        )
        data = resp.json()
        assert "resource_response" in data
        pin = data["resource_response"]["data"]
        assert "id" in pin

        # Store for cleanup
        self.__class__._created_pin_id = pin["id"]

    def test_delete_pin(self, pinterest):
        pin_id = getattr(self.__class__, "_created_pin_id", None)
        if pin_id is None:
            pytest.skip("No pin was created to delete")
        resp = pinterest.delete_pin(pin_id=pin_id)
        assert resp.status_code == 200

    def test_repin(self, pinterest, test_board):
        """Repin an existing pin from search."""
        results = pinterest.search(scope="pins", query="nature wallpaper", page_size=5, reset_bookmark=True)
        if not results:
            pytest.skip("No search results to repin")

        resp = pinterest.repin(board_id=test_board["id"], pin_id=results[0]["id"])
        data = resp.json()
        assert "resource_response" in data
        repin = data["resource_response"]["data"]

        # Cleanup
        if "id" in repin:
            pinterest.delete_pin(pin_id=repin["id"])


class TestUploadPin:

    def test_upload_pin(self, pinterest, test_board):
        """Upload a local image file as a pin."""
        # Create a minimal valid PNG file
        import struct
        import zlib

        def make_png():
            """Create a 1x1 red PNG."""
            raw_data = b'\x00\xff\x00\x00'  # filter byte + RGB
            compressed = zlib.compress(raw_data)

            def chunk(chunk_type, data):
                c = chunk_type + data
                return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

            sig = b'\x89PNG\r\n\x1a\n'
            ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            idat = chunk(b'IDAT', compressed)
            iend = chunk(b'IEND', b'')
            return sig + ihdr + idat + iend

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(make_png())
            tmp_path = f.name

        try:
            resp = pinterest.upload_pin(
                board_id=test_board["id"],
                image_file=tmp_path,
                description="Upload test pin",
                title="Upload Test",
            )
            data = resp.json()
            assert "resource_response" in data
            pin = data["resource_response"]["data"]
            assert "id" in pin

            # Cleanup
            pinterest.delete_pin(pin_id=pin["id"])
        finally:
            os.unlink(tmp_path)


class TestCommentActions:

    def test_comment_and_delete(self, pinterest, owned_pin):
        """Create a comment on our own pin, then delete it."""
        pin_id = owned_pin["id"]

        resp = pinterest.comment(pin_id=pin_id, text="Integration test comment")
        data = resp.json()
        assert "resource_response" in data
        comment = data["resource_response"]["data"]
        assert "id" in comment

        # Delete the comment
        resp = pinterest.delete_comment(pin_id=pin_id, comment_id=comment["id"])
        assert resp.status_code == 200

    def test_get_comments_all(self, pinterest, owned_pin):
        """get_comments_all wraps get_comments in a loop."""
        result = pinterest.get_comments_all(pin_id=owned_pin["id"])
        assert isinstance(result, list)


