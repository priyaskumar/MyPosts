from fastapi.testclient import TestClient
import pytest

# to set up the sqlalchemy database url
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# get_db is overriden to create a separate database for testing
from app.database import get_db
from app.main import app
from app.database import Base

from app.oauth2 import create_access_token
from app import models

# uncomment the below import line to create databases using alembic 
# versions rather than following the sqlalchemy database setup

# from alembic import command  


# setting up sqlalchemy database url
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    # command.downgrade("base")
    Base.metadata.drop_all(bind=engine)
    # command.upgrade("base")
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# client fixture is dependant on session fixture
# session fixture is run first
# 1. the older tables are dropped and new empty tables are created
# 2. get_db dependancy is overriden by override_get_db in order to have a separate database for testing
# 3. returns the app instance with above database 
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# client fixture runs first
# 1. creates a new user via create_user path operation
# 2. validates the status code i.e. checks if creation of new user was successful
# 3. returns the new_user details
@pytest.fixture
def test_user(client):
    user_data = {"email": "pytest@gmail.com",
                 "password": "pwd123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# this is fixture to create another user
@pytest.fixture
def test_user2(client):
    user_data = {"email": "pytest123@gmail.com",
                 "password": "pwd123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


# this fixture is dependant on test_user
# creates a valid jwt token for the user credentials created in test_user fixture
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


# this fixture is dependant on both client and token 
# creates an instance of client with valid jwt token 
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

# this fixture is dependant on test_user, test_user2, session
# creates few posts on which the posts path operations are tested
@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts