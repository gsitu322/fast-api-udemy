from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette import status

from ..models import Todos, Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient

import pytest

# sqlite setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///testdb.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "gsitu322", "id": 1, "role": "admin"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE from todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Learn to code",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Learn to code",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
