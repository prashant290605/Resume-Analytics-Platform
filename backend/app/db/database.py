from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from backend.app.core.config import get_settings


class Database:
    def __init__(self, db_path: Path | str | None = None):
        self.db_path = str(db_path if db_path is not None else get_settings().database_path)
        self._initialise()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialise(self) -> None:
        with self.connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS batches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    raw_text TEXT NOT NULL,
                    file_name TEXT,
                    file_path TEXT,
                    parsed_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id INTEGER,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    parsed_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS screenings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER NOT NULL,
                    batch_id INTEGER,
                    threshold REAL NOT NULL,
                    embedding_provider TEXT NOT NULL,
                    status TEXT NOT NULL,
                    total_candidates INTEGER NOT NULL DEFAULT 0,
                    shortlisted_count INTEGER NOT NULL DEFAULT 0,
                    average_score REAL NOT NULL DEFAULT 0,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
                    FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    screening_id INTEGER NOT NULL,
                    resume_id INTEGER NOT NULL,
                    score REAL NOT NULL,
                    semantic_score REAL NOT NULL,
                    skill_score REAL NOT NULL,
                    experience_score REAL NOT NULL,
                    shortlisted INTEGER NOT NULL DEFAULT 0,
                    breakdown_json TEXT NOT NULL,
                    email_json TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (screening_id) REFERENCES screenings (id) ON DELETE CASCADE,
                    FOREIGN KEY (resume_id) REFERENCES resumes (id) ON DELETE CASCADE
                );
                """
            )
            self._ensure_column(conn, "resumes", "batch_id", "INTEGER REFERENCES batches(id) ON DELETE SET NULL")
            self._ensure_column(conn, "screenings", "batch_id", "INTEGER REFERENCES batches(id) ON DELETE SET NULL")
            conn.executescript(
                """
                CREATE INDEX IF NOT EXISTS idx_matches_screening ON matches (screening_id);
                CREATE INDEX IF NOT EXISTS idx_matches_resume ON matches (resume_id);
                CREATE INDEX IF NOT EXISTS idx_resumes_batch ON resumes (batch_id);
                CREATE INDEX IF NOT EXISTS idx_screenings_job ON screenings (job_id);
                CREATE INDEX IF NOT EXISTS idx_screenings_batch ON screenings (batch_id);
                """
            )

    def _ensure_column(self, conn: sqlite3.Connection, table_name: str, column_name: str, definition: str) -> None:
        existing_columns = {
            row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in existing_columns:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
