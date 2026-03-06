import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))

from app import app, init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_list_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert "users" in data


def test_get_user(client):
    response = client.get("/user?username=alice")
    assert response.status_code == 200
