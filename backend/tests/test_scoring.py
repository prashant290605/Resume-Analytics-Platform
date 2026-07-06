from __future__ import annotations

import pytest

from backend.app.services.embeddings import MatchingEngine


@pytest.fixture()
def engine() -> MatchingEngine:
    eng = MatchingEngine()
    eng.ollama_provider.is_available = lambda: False  # deterministic TF-IDF path
    return eng


JOB = {
    "title": "Backend Engineer",
    "parsed": {
        "required_skills": ["Python", "FastAPI", "SQL", "Docker", "AWS"],
        "years_experience_required": {"minimum": 4, "label": "4 years"},
        "education": "Bachelor",
        "responsibilities": ["Build APIs", "Work with cloud infrastructure"],
        "raw_jd": "Backend Engineer using Python FastAPI SQL Docker AWS building APIs and services.",
    },
}


def make_resume(skills: list[str], years: int, summary: str) -> dict:
    return {
        "name": "Candidate",
        "summary": summary,
        "skills": skills,
        "work_experience": f"{years} years of experience.",
        "education": "Bachelor of Engineering",
        "certifications": [],
        "years_experience": years,
    }


class TestHybridScoring:
    def test_strong_match_scores_above_threshold(self, engine):
        resume = make_resume(
            ["Python", "FastAPI", "SQL", "Docker", "AWS"], 4,
            "Backend engineer building Python FastAPI services on AWS with Docker and SQL.",
        )
        computation = engine.debug_score(JOB, resume)
        assert computation.score > 70.0

    def test_weak_match_scores_below_strong_match(self, engine):
        strong = make_resume(
            ["Python", "FastAPI", "SQL", "Docker", "AWS"], 4,
            "Backend engineer building Python FastAPI services on AWS.",
        )
        weak = make_resume(
            ["Photoshop", "Illustrator"], 1,
            "Graphic designer creating brand identities and print layouts.",
        )
        assert engine.debug_score(JOB, strong).score > engine.debug_score(JOB, weak).score

    def test_matched_and_missing_skills_are_disjoint(self, engine):
        resume = make_resume(["Python", "SQL"], 2, "Python developer writing SQL pipelines.")
        computation = engine.debug_score(JOB, resume)
        assert set(computation.matched_skills).isdisjoint(computation.missing_skills)
        assert "Python" in computation.matched_skills
        assert "Docker" in computation.missing_skills

    def test_score_is_bounded(self, engine):
        resume = make_resume(["Python", "FastAPI", "SQL", "Docker", "AWS"], 10, JOB["parsed"]["raw_jd"])
        computation = engine.debug_score(JOB, resume)
        assert 0.0 <= computation.score <= 100.0

    def test_batch_scoring_preserves_order(self, engine):
        resumes = [
            {"id": 1, "parsed": make_resume(["Python"], 1, "Python beginner.")},
            {"id": 2, "parsed": make_resume(["Python", "FastAPI", "SQL", "Docker", "AWS"], 5, "Senior backend engineer, Python FastAPI AWS Docker SQL.")},
        ]
        provider, computations = engine.score_candidates(JOB, resumes)
        assert provider == "local_tfidf"
        assert len(computations) == 2
        assert computations[1].score > computations[0].score
