"""Unit tests for the DevSecOps Security Gate API."""

from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import NoteCreate, app, create_note


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient for the FastAPI application."""
    return TestClient(app)


def test_read_root(client: TestClient) -> None:
    """The root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Welcome")


def test_read_health(client: TestClient) -> None:
    """The health endpoint reports a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_note(client: TestClient) -> None:
    """A valid POST request creates a note."""
    payload = {"title": "Security Gate", "content": "Automated checks are running."}
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data


def test_create_note_validates_input(client: TestClient) -> None:
    """The create-note endpoint rejects invalid input."""
    response = client.post("/notes", json={"title": "", "content": ""})
    assert response.status_code == 422


def test_read_note(client: TestClient) -> None:
    """A note can be retrieved by its ID."""
    payload = {"title": "Test Note", "content": "Test content."}
    create_response = client.post("/notes", json=payload)
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


def test_read_missing_note(client: TestClient) -> None:
    """Requesting a non-existent note returns 404."""
    response = client.get("/notes/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_concurrent_note_creation_assigns_unique_ids() -> None:
    """Parallel calls must not overwrite notes with duplicate IDs."""
    def create(index: int) -> int:
        return create_note(NoteCreate(title=f"Note {index}", content="Concurrent test")).id

    with ThreadPoolExecutor(max_workers=16) as pool:
        ids = list(pool.map(create, range(100)))

    assert len(ids) == len(set(ids))
