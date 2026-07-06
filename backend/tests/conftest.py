from __future__ import annotations

import sys
from pathlib import Path

import fitz
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from backend.app.core import config as config_module  # noqa: E402
from backend.app.core.config import Settings, get_settings  # noqa: E402
from backend.app.db.database import Database  # noqa: E402
from backend.app.db.repository import ScreeningRepository  # noqa: E402


@pytest.fixture()
def settings(tmp_path, monkeypatch) -> Settings:
    """Isolated settings pointing all storage at a temp directory."""
    monkeypatch.setenv("RAP_DATA_DIR", str(tmp_path / "data"))
    get_settings.cache_clear()
    yield get_settings()
    get_settings.cache_clear()


@pytest.fixture()
def database(settings) -> Database:
    return Database(settings.database_path)


@pytest.fixture()
def repository(database) -> ScreeningRepository:
    return ScreeningRepository(database)


@pytest.fixture()
def client(settings) -> TestClient:
    from backend.app.main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def sample_resume_pdf(tmp_path) -> Path:
    """Generate a small, realistic PDF resume on the fly."""
    path = tmp_path / "alex_candidate.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        "Alex Candidate\n"
        "alex.candidate@example.com | +1 555 010 1234\n"
        "Summary: Backend engineer building Python FastAPI services on AWS.\n"
        "Skills: Python, FastAPI, SQL, Docker, AWS, Git\n"
        "Experience: 4 years building Python APIs with Docker on AWS.\n"
        "Education: Bachelor of Engineering in Computer Science\n",
        fontsize=11,
    )
    doc.save(path)
    doc.close()
    return path


JOB_DESCRIPTION = (
    "We are hiring a Backend Engineer with 3+ years of experience. "
    "Required skills: Python, FastAPI, SQL, Docker, AWS. "
    "You will build REST APIs and work with cloud infrastructure."
)
