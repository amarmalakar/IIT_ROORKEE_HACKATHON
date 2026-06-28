"""Tests for FastAPI routes."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_personas():
    response = client.get("/api/persona")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert data[0]["id"]


def test_list_models():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]


def test_list_languages():
    response = client.get("/api/languages")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_get_workflow():
    response = client.get("/api/workflow")
    assert response.status_code == 200
    data = response.json()
    assert len(data["nodes"]) == 13
    assert len(data["edges"]) == 14


def test_websocket_removed():
    with pytest.raises(Exception):
        with client.websocket_connect("/api/chat"):
            pass
