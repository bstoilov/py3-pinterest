"""Tests for conversation/message API calls."""
import pytest


def test_get_conversations(pinterest):
    result = pinterest.get_conversations()
    assert isinstance(result, list)


def test_initiate_conversation_and_send_message(pinterest):
    """Initiate a conversation with another user and send a message."""
    # Get own user id
    user_data = pinterest.get_user_overview()
    own_user_id = user_data["id"]

    # Find another user via search
    results = pinterest.search(scope="pins", query="art", page_size=10, reset_bookmark=True)
    other_user_id = None
    for r in results:
        if "pinner" in r and "id" in r["pinner"] and r["pinner"]["id"] != own_user_id:
            other_user_id = r["pinner"]["id"]
            break
    if other_user_id is None:
        pytest.skip("Could not find another user for conversation test")

    resp = pinterest.initiate_conversation(user_ids=[own_user_id, other_user_id])
    data = resp.json()
    assert "resource_response" in data
    conversation = data["resource_response"]["data"]
    conversation_id = conversation["id"]

    # Send a follow-up message
    resp = pinterest.send_message(message="integration test", conversation_id=conversation_id)
    assert resp.status_code == 200

    # Load the conversation messages
    messages = pinterest.load_conversation(conversation_id=conversation_id)
    assert isinstance(messages, list)
    assert len(messages) >= 1
