from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings, overridable via environment variables (prefix RAP_) or a .env file."""

    model_config = SettingsConfigDict(env_prefix="RAP_", env_file=".env", extra="ignore")

    # Storage
    data_dir: Path = BASE_DIR / "data"

    # Embeddings
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "nomic-embed-text"

    # Screening
    default_shortlist_threshold: float = 70.0

    # HTTP
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    max_upload_bytes: int = 5 * 1024 * 1024  # 5 MiB per file
    enable_metrics: bool = True

    # Logging
    log_level: str = "INFO"

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def job_upload_dir(self) -> Path:
        return self.uploads_dir / "jobs"

    @property
    def resume_upload_dir(self) -> Path:
        return self.uploads_dir / "resumes"

    @property
    def database_path(self) -> Path:
        return self.data_dir / "resume_analytics.db"

    def ensure_directories(self) -> None:
        for path in (self.data_dir, self.uploads_dir, self.job_upload_dir, self.resume_upload_dir):
            path.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
