from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app import oauth2, models
import pytest


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user1(client, session):
    user_data = {"username": "newnew", "password": "nice to1"}
    res = client.post("/", json=user_data)
    created_user = res.json()
    assert res.status_code == 201
    created_user['password'] = user_data["password"]
    created_user['id'] = session.query(models.User).filter(models.User.username == created_user['username']).first().id
    return created_user


@pytest.fixture
def test_user2(client, session):
    user_data = {"username": "user2", "password": "nice one!"}
    res = client.post("/", json=user_data)
    created_user = res.json()
    assert res.status_code == 201
    created_user['password'] = user_data["password"]
    created_user['id'] = session.query(models.User).filter(models.User.username == created_user['username']).first().id
    return created_user


@pytest.fixture
def token(test_user1):
    return oauth2.create_token(data={'username': test_user1['username']})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def create_test_messages(test_user1, test_user2, session):
    user1_id = test_user1['id']
    user2_id = test_user2['id']
    messages = [
        ("Hello, how are you?", user1_id, user2_id),
        ("I'm good, thanks!", user2_id, user1_id),
        ("What are you doing?", user1_id, user2_id),
        ("Nothing much, just relaxing.", user2_id, user1_id),
        ("Let's meet up later.", user1_id, user2_id),
        ("Sure, where do you want to meet?", user2_id, user1_id),
        ("How was your day?", user1_id, user2_id),
        ("It was good, and yours?", user2_id, user1_id),
        ("I had a busy day.", user1_id, user2_id),
        ("Hope you have a relaxing evening.", user2_id, user1_id)
    ]
    for content, sender, receiver in messages:
        message = models.Message(owner_id=sender, receiver_id=receiver, content=content)
        session.add(message)
    session.commit()
    messages = session.query(models.Message).all()
    return messages


