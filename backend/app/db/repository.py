from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from backend.app.db.database import Database


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ScreeningRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_batch(self, name: str) -> dict[str, Any]:
        created_at = utc_now()
        with self.database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO batches (name, status, created_at)
                VALUES (?, 'active', ?)
                """,
                (name, created_at),
            )
        return self.get_batch(cursor.lastrowid)

    def get_batch(self, batch_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute("SELECT * FROM batches WHERE id = ?", (batch_id,)).fetchone()
        return dict(row) if row else None

    def list_batches(self) -> list[dict[str, Any]]:
        with self.database.connection() as conn:
            rows = conn.execute("SELECT * FROM batches ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def create_job(
        self,
        title: str,
        source_type: str,
        raw_text: str,
        parsed: dict[str, Any],
        file_name: str | None = None,
        file_path: str | None = None,
    ) -> dict[str, Any]:
        created_at = utc_now()
        with self.database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO jobs (title, source_type, raw_text, file_name, file_path, parsed_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (title, source_type, raw_text, file_name, file_path, json.dumps(parsed), created_at),
            )
            job_id = cursor.lastrowid
        return self.get_job(job_id)

    def list_jobs(self) -> list[dict[str, Any]]:
        with self.database.connection() as conn:
            rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
        return [self._job_row(row) for row in rows]

    def get_job(self, job_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return self._job_row(row) if row else None

    def create_resume(self, file_name: str, file_path: str, parsed: dict[str, Any], batch_id: int | None = None) -> dict[str, Any]:
        created_at = utc_now()
        with self.database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO resumes (batch_id, file_name, file_path, parsed_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (batch_id, file_name, file_path, json.dumps(parsed), created_at),
            )
            resume_id = cursor.lastrowid
        return self.get_resume(resume_id)

    def list_resumes(self, batch_id: int | None = None) -> list[dict[str, Any]]:
        with self.database.connection() as conn:
            if batch_id is None:
                rows = conn.execute("SELECT * FROM resumes ORDER BY created_at DESC").fetchall()
            else:
                rows = conn.execute("SELECT * FROM resumes WHERE batch_id = ? ORDER BY created_at DESC", (batch_id,)).fetchall()
        return [self._resume_row(row) for row in rows]

    def get_resume(self, resume_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,)).fetchone()
        return self._resume_row(row) if row else None

    def create_screening(self, job_id: int, threshold: float, embedding_provider: str, batch_id: int | None = None) -> int:
        with self.database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO screenings (job_id, batch_id, threshold, embedding_provider, status, started_at)
                VALUES (?, ?, ?, ?, 'running', ?)
                """,
                (job_id, batch_id, threshold, embedding_provider, utc_now()),
            )
            return cursor.lastrowid

    def complete_screening(
        self,
        screening_id: int,
        total_candidates: int,
        shortlisted_count: int,
        average_score: float,
    ) -> None:
        with self.database.connection() as conn:
            conn.execute(
                """
                UPDATE screenings
                SET status = 'completed',
                    total_candidates = ?,
                    shortlisted_count = ?,
                    average_score = ?,
                    completed_at = ?
                WHERE id = ?
                """,
                (total_candidates, shortlisted_count, average_score, utc_now(), screening_id),
            )

    def add_match(
        self,
        screening_id: int,
        resume_id: int,
        score: float,
        semantic_score: float,
        skill_score: float,
        experience_score: float,
        shortlisted: bool,
        breakdown: dict[str, Any],
        generated_email: str | None,
    ) -> None:
        with self.database.connection() as conn:
            conn.execute(
                """
                INSERT INTO matches (
                    screening_id, resume_id, score, semantic_score, skill_score, experience_score,
                    shortlisted, breakdown_json, email_json, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    screening_id,
                    resume_id,
                    score,
                    semantic_score,
                    skill_score,
                    experience_score,
                    int(shortlisted),
                    json.dumps(breakdown),
                    json.dumps({"content": generated_email}) if generated_email else None,
                    utc_now(),
                ),
            )

    def get_latest_screening(self) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT s.*, j.title AS job_title
                FROM screenings s
                JOIN jobs j ON j.id = s.job_id
                ORDER BY s.started_at DESC
                LIMIT 1
                """
            ).fetchone()
        return dict(row) if row else None

    def get_screening(self, screening_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT s.*, j.title AS job_title
                FROM screenings s
                JOIN jobs j ON j.id = s.job_id
                WHERE s.id = ?
                """,
                (screening_id,),
            ).fetchone()
        return dict(row) if row else None

    def get_latest_screening_for_batch(self, batch_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT s.*, j.title AS job_title
                FROM screenings s
                JOIN jobs j ON j.id = s.job_id
                WHERE s.batch_id = ?
                ORDER BY s.started_at DESC
                LIMIT 1
                """,
                (batch_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_matches(self, screening_id: int) -> list[dict[str, Any]]:
        with self.database.connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    m.*,
                    r.file_name,
                    r.parsed_json,
                    s.job_id,
                    j.title AS job_title
                FROM matches m
                JOIN resumes r ON r.id = m.resume_id
                JOIN screenings s ON s.id = m.screening_id
                JOIN jobs j ON j.id = s.job_id
                WHERE m.screening_id = ?
                ORDER BY m.score DESC
                """,
                (screening_id,),
            ).fetchall()
        return [self._match_row(row) for row in rows]

    def get_batch_results(self, batch_id: int) -> dict[str, Any] | None:
        screening = self.get_latest_screening_for_batch(batch_id)
        if not screening:
            return None
        return {
            "batch": self.get_batch(batch_id),
            "screening": screening,
            "matches": self.list_matches(screening["id"]),
        }

    def get_candidate_detail(self, screening_id: int, resume_id: int) -> dict[str, Any] | None:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT
                    m.*,
                    r.parsed_json,
                    r.file_name,
                    j.title AS job_title
                FROM matches m
                JOIN resumes r ON r.id = m.resume_id
                JOIN screenings s ON s.id = m.screening_id
                JOIN jobs j ON j.id = s.job_id
                WHERE m.screening_id = ? AND m.resume_id = ?
                """,
                (screening_id, resume_id),
            ).fetchone()
        return self._match_row(row) if row else None

    def dashboard_metrics(self) -> dict[str, Any]:
        with self.database.connection() as conn:
            totals = conn.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM resumes) AS total_resumes,
                    (SELECT COUNT(*) FROM screenings) AS screenings_run,
                    COALESCE((SELECT SUM(shortlisted_count) FROM screenings), 0) AS shortlisted_candidates,
                    COALESCE((SELECT AVG(score) FROM matches), 0) AS average_match_score
                """
            ).fetchone()
        latest = self.get_latest_screening()
        return {
            "total_resumes": totals["total_resumes"],
            "screenings_run": totals["screenings_run"],
            "shortlisted_candidates": totals["shortlisted_candidates"],
            "average_match_score": round(totals["average_match_score"], 2),
            "latest_job_title": latest["job_title"] if latest else None,
            "latest_screening_id": latest["id"] if latest else None,
            "embedding_provider": latest["embedding_provider"] if latest else "pending",
        }

    def _job_row(self, row: Any) -> dict[str, Any]:
        payload = dict(row)
        payload["parsed"] = json.loads(payload.pop("parsed_json"))
        return payload

    def _resume_row(self, row: Any) -> dict[str, Any]:
        payload = dict(row)
        payload["parsed"] = json.loads(payload.pop("parsed_json"))
        return payload

    def _match_row(self, row: Any) -> dict[str, Any]:
        payload = dict(row)
        parsed = json.loads(payload.pop("parsed_json"))
        breakdown = json.loads(payload.pop("breakdown_json"))
        email_json = payload.pop("email_json")
        payload["parsed_resume"] = parsed
        payload["breakdown"] = breakdown
        payload["generated_email"] = json.loads(email_json)["content"] if email_json else None
        return payload
