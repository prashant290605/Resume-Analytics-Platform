from __future__ import annotations

import logging
from statistics import mean
from typing import Any

from fastapi import HTTPException

from backend.app.db.repository import ScreeningRepository
from backend.app.services.emailer import generate_interview_email
from backend.app.services.embeddings import MatchingEngine


logger = logging.getLogger(__name__)


class ScreeningService:
    def __init__(self, repository: ScreeningRepository, matching_engine: MatchingEngine | None = None):
        self.repository = repository
        self.matching_engine = matching_engine or MatchingEngine()

    def run_screening(self, job_id: int, threshold: float, generate_emails: bool, batch_id: int | None = None) -> dict[str, Any]:
        job = self.repository.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job description not found.")

        if batch_id is not None and not self.repository.get_batch(batch_id):
            raise HTTPException(status_code=404, detail="Batch not found.")

        resumes = self.repository.list_resumes(batch_id=batch_id)
        if not resumes:
            raise HTTPException(status_code=400, detail="Upload at least one resume before running screening.")

        provider_name, computations = self.matching_engine.score_candidates(job, resumes)
        screening_id = self.repository.create_screening(
            job_id=job_id,
            threshold=threshold,
            embedding_provider=provider_name,
            batch_id=batch_id,
        )

        candidates: list[dict[str, Any]] = []
        for resume, computation in zip(resumes, computations, strict=True):
            logger.debug(
                "score resume_id=%s batch_id=%s skill=%.2f semantic=%.2f experience=%.2f final=%.2f",
                resume["id"], batch_id, computation.skill_score,
                computation.semantic_score, computation.experience_score, computation.score,
            )
            shortlisted = computation.score >= threshold
            email_content = None
            if generate_emails and shortlisted:
                email_content = generate_interview_email(
                    candidate_name=resume["parsed"].get("name", "Candidate"),
                    job_title=job["title"],
                    matched_skills=computation.matched_skills,
                )

            breakdown = {
                "matched_skills": computation.matched_skills,
                "missing_skills": computation.missing_skills,
                "semantic_score": computation.semantic_score,
                "skill_score": computation.skill_score,
                "experience_score": computation.experience_score,
                "years_experience": resume["parsed"].get("years_experience", 0),
                "summary": resume["parsed"].get("summary", ""),
            }

            self.repository.add_match(
                screening_id=screening_id,
                resume_id=resume["id"],
                score=computation.score,
                semantic_score=computation.semantic_score,
                skill_score=computation.skill_score,
                experience_score=computation.experience_score,
                shortlisted=shortlisted,
                breakdown=breakdown,
                generated_email=email_content,
            )

            candidates.append(
                {
                    "resume_id": resume["id"],
                    "screening_id": screening_id,
                    "name": resume["parsed"].get("name", "Unknown Candidate"),
                    "email": resume["parsed"].get("email"),
                    "score": computation.score,
                    "semantic_score": computation.semantic_score,
                    "skill_score": computation.skill_score,
                    "experience_score": computation.experience_score,
                    "skills": resume["parsed"].get("skills", []),
                    "years_experience": float(resume["parsed"].get("years_experience", 0.0)),
                    "shortlisted": shortlisted,
                    "matched_skills": computation.matched_skills,
                    "missing_skills": computation.missing_skills,
                    "job_title": job["title"],
                }
            )

        candidates.sort(key=lambda item: item["score"], reverse=True)
        shortlisted_count = sum(1 for candidate in candidates if candidate["shortlisted"])
        average_score = round(mean(candidate["score"] for candidate in candidates), 2) if candidates else 0.0
        self.repository.complete_screening(
            screening_id=screening_id,
            total_candidates=len(candidates),
            shortlisted_count=shortlisted_count,
            average_score=average_score,
        )

        return {
            "screening_id": screening_id,
            "job_id": job_id,
            "batch_id": batch_id,
            "job_title": job["title"],
            "total_candidates": len(candidates),
            "shortlisted_count": shortlisted_count,
            "average_score": average_score,
            "embedding_provider": provider_name,
            "candidates": candidates,
        }

    def get_results(self, screening_id: int | None = None) -> dict[str, Any]:
        screening = self.repository.get_screening(screening_id) if screening_id else self.repository.get_latest_screening()
        if not screening:
            return {
                "screening_id": None,
                "job_id": None,
                "batch_id": None,
                "job_title": None,
                "threshold": None,
                "embedding_provider": None,
                "candidates": [],
            }

        matches = self.repository.list_matches(screening["id"])
        candidates = [
            {
                "resume_id": match["resume_id"],
                "screening_id": screening["id"],
                "name": match["parsed_resume"].get("name", "Unknown Candidate"),
                "email": match["parsed_resume"].get("email"),
                "score": round(match["score"], 2),
                "semantic_score": round(match["semantic_score"], 2),
                "skill_score": round(match["skill_score"], 2),
                "experience_score": round(match["experience_score"], 2),
                "skills": match["parsed_resume"].get("skills", []),
                "years_experience": float(match["parsed_resume"].get("years_experience", 0.0)),
                "shortlisted": bool(match["shortlisted"]),
                "matched_skills": match["breakdown"].get("matched_skills", []),
                "missing_skills": match["breakdown"].get("missing_skills", []),
                "job_title": screening["job_title"],
            }
            for match in matches
        ]
        return {
            "screening_id": screening["id"],
            "job_id": screening["job_id"],
            "batch_id": screening.get("batch_id"),
            "job_title": screening["job_title"],
            "threshold": float(screening["threshold"]),
            "embedding_provider": screening["embedding_provider"],
            "candidates": candidates,
        }

    def get_candidate_detail(self, screening_id: int, resume_id: int) -> dict[str, Any]:
        match = self.repository.get_candidate_detail(screening_id=screening_id, resume_id=resume_id)
        if not match:
            raise HTTPException(status_code=404, detail="Candidate result not found for this screening.")

        return {
            "resume_id": resume_id,
            "screening_id": screening_id,
            "job_title": match["job_title"],
            "score": round(match["score"], 2),
            "shortlisted": bool(match["shortlisted"]),
            "parsed_resume": match["parsed_resume"],
            "match_breakdown": match["breakdown"],
            "generated_email": match["generated_email"],
        }
