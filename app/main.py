"""Small FastAPI application for the DevSecOps security gate project.

This application is intentionally simple. It provides a basic note-taking API
used to demonstrate automated security testing in GitHub Actions.
"""

from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="DevSecOps Security Gate API",
    description="A small API demonstrating automated DevSecOps security controls.",
    version="0.1.0",
)

# In-memory store for demonstration purposes only.
_notes: dict[int, dict] = {}
_note_id_counter = 0
_notes_lock = Lock()


class NoteCreate(BaseModel):
    """Request model for creating a new note."""

    title: str = Field(..., min_length=1, max_length=120, description="Title of the note.")
    content: str = Field(..., min_length=1, max_length=4000, description="Content of the note.")


class Note(BaseModel):
    """Response model representing a stored note."""

    id: int
    title: str
    content: str


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a welcome message."""
    return {"message": "Welcome to the DevSecOps Security Gate API."}


@app.get("/health")
def read_health() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "healthy"}


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: NoteCreate) -> Note:
    """Create a new note and return it with an assigned ID."""
    global _note_id_counter
    with _notes_lock:
        _note_id_counter += 1
        new_note = {"id": _note_id_counter, "title": note.title, "content": note.content}
        _notes[_note_id_counter] = new_note
    return Note(**new_note)


@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int) -> Note:
    """Retrieve a note by its ID."""
    with _notes_lock:
        note = _notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return Note(**note)
