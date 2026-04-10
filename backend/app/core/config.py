from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
JOB_UPLOAD_DIR = UPLOADS_DIR / "jobs"
RESUME_UPLOAD_DIR = UPLOADS_DIR / "resumes"
DATABASE_PATH = DATA_DIR / "resume_analytics.db"

OLLAMA_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_SHORTLIST_THRESHOLD = 70.0

for path in (DATA_DIR, UPLOADS_DIR, JOB_UPLOAD_DIR, RESUME_UPLOAD_DIR):
    path.mkdir(parents=True, exist_ok=True)
