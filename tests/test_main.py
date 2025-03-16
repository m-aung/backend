import os
import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        "POSTGRESQL_CONNECTION_DEV": "postgresql://devuser1:password-DEV@localhost:5433/dev_db_1",
        "POSTGRESQL_CONNECTION_AWS": "postgresql://aws_user:aws_pass@aws_host/aws_db",
        "POSTGRESQL_CONNECTION_AZURE": "postgresql://azure_user:azure_pass@azure_host/azure_db",
        "APP_ENV": "dev"
    }):
        yield

def test_get_users(mock_env_vars):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user(mock_env_vars):
    new_user = {
      "first_name": "Peter",
      "last_name": "Parker",
      "email": "peter.parker.93@example.com",
      "phone": None,
      "role": "owner",
      "password_hash": "hashedpassword"
    }
    new_user_response = client.post("/users", json=new_user)
    user_id = new_user_response.json()["id"]
    response = client.get(f"/users/id={user_id}")
    if response.status_code == 200:
        assert response.json()["id"] == user_id
        # cleanup
        client.delete(f"users/{user_id}")
    else:
        assert response.status_code == 404


def test_create_user(mock_env_vars):
    test_email = "john.doe@example.com" 
    new_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": test_email,
        "phone": "1234567890",
        "role": "owner",
        "password_hash": "hashedpassword"
    }
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    assert response.json()["email"] == "john.doe@example.com"
    user_id = response.json()["id"]
    delete_response = client.delete(f"users/{user_id}")
    assert delete_response.status_code == 200

def test_update_user(mock_env_vars):
    updated_user = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "0987654321",
        "role": "user"
    }
    response = client.put("/users/1", json=updated_user)
    if response.status_code == 200:
        assert response.json()["email"] == "jane.doe@example.com"
    else:
        assert response.status_code == 404

def test_delete_user(mock_env_vars):
    response = client.delete("/users/1")
    if response.status_code == 200:
        assert response.json()["message"] == "User deleted successfully"
    else:
        assert response.status_code == 404