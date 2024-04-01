from app import schemas
from app.config import settings
from jose import jwt, JWTError
import pytest


def test_root(client):
    res = client.get("/")
    assert "hello" == res.json()


def test_login_user(client, test_user1):
    res = client.post("/login", data={"username": test_user1["username"], "password": test_user1["password"]})
    # created_user = schemas.UserBase(**res.json())
    login_res = schemas.Token(**res.json())
    access_token = login_res.access_token
    token_type = login_res.token_type
    payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
    username = payload.get("username")

    assert token_type == 'bearer'
    assert username == test_user1['username']
    assert res.status_code == 200


@pytest.mark.parametrize("username, password, status_code", [
    ('wrong', 'password123', 403),
    ('san', 'wrongpassword', 403),
    ('wro', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sa', None, 422)
])
def test_incorrect_login(client, test_user1, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == status_code
