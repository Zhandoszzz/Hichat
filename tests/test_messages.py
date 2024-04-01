from app import models
from app import schemas
from app.config import settings
from jose import jwt, JWTError
import pytest


def test_all_messages(authorized_client, test_user1, test_user2, create_test_messages):
    res = authorized_client.get(f"/chat/{test_user2['username']}")
    assert len(res.json()) == len(create_test_messages)


def test_create_message(authorized_client, test_user1, test_user2, session):
    username = test_user2['username']
    res = authorized_client.post(f"/chat/{username}", params={
        'content': 'Hello!'
    })
    message = res.json()
    assert message['owner_id'] == test_user1['id']
    assert message['receiver_id'] == test_user2['id']
    assert message['content'] == 'Hello!'
