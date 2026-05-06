"""Top-level module exposing the FastAPI `app` for uvicorn.

This file allows running the project with `uvicorn main:app` from
the repository root (for example in development with `--reload`).
"""

from app.api import app
