from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_update_todo():
    response = client.put("/todos/1", json={"title": "Updated Todo", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"

def test_delete_todo():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"