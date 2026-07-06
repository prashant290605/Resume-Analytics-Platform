from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

import numpy as np
import requests
from backend.app.core.config import get_settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class EmbeddingProvider(Protocol):
    name: str

    def vectorize(self, job_text: str, resume_texts: list[str]) -> tuple[np.ndarray, np.ndarray]:
        ...


class OllamaEmbeddingProvider:
    name = "ollama"

    def __init__(self, base_url: str | None = None, model: str | None = None):
        settings = get_settings()
        base_url = base_url or settings.ollama_base_url
        model = model or settings.ollama_model
        self.base_url = base_url.rstrip("/")
        self.model = model

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=1.5)
            return response.ok
        except requests.RequestException:
            return False

    def _embed(self, text: str) -> np.ndarray:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model, "prompt": text},
            timeout=30,
        )
        response.raise_for_status()
        return np.array(response.json()["embedding"], dtype=float)

    def vectorize(self, job_text: str, resume_texts: list[str]) -> tuple[np.ndarray, np.ndarray]:
        job_vector = self._embed(job_text)
        resume_vectors = np.vstack([self._embed(text) for text in resume_texts])
        return job_vector, resume_vectors


class TfidfEmbeddingProvider:
    name = "local_tfidf"

    def vectorize(self, job_text: str, resume_texts: list[str]) -> tuple[np.ndarray, np.ndarray]:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([job_text, *resume_texts]).toarray()
        return matrix[0], matrix[1:]


def normalize_similarity(similarity: float) -> float:
    clipped = max(0.0, min(1.0, similarity))
    return min(1.0, max(0.15, clipped))


@dataclass
class MatchComputation:
    score: float
    semantic_score: float
    skill_score: float
    experience_score: float
    matched_skills: list[str]
    missing_skills: list[str]


class MatchingEngine:
    def __init__(self) -> None:
        self.ollama_provider = OllamaEmbeddingProvider()
        self.fallback_provider = TfidfEmbeddingProvider()

    def active_provider(self) -> EmbeddingProvider:
        return self.ollama_provider if self.ollama_provider.is_available() else self.fallback_provider

    def score_candidates(self, job: dict, resumes: list[dict]) -> tuple[str, list[MatchComputation]]:
        provider = self.active_provider()
        job_text = build_job_embedding_text(job)
        resume_texts = [build_resume_embedding_text(resume["parsed"]) for resume in resumes]
        job_vector, resume_vectors = provider.vectorize(job_text, resume_texts)

        if resume_vectors.size == 0:
            return provider.name, []

        semantic_scores = cosine_similarity([job_vector], resume_vectors)[0]
        computations: list[MatchComputation] = []
        required_skills = set(skill.lower() for skill in job["parsed"].get("required_skills", []))
        required_years = float(job["parsed"].get("years_experience_required", {}).get("minimum", 0.0))

        for index, resume in enumerate(resumes):
            parsed_resume = resume["parsed"]
            candidate_skills = set(skill.lower() for skill in parsed_resume.get("skills", []))
            matched = sorted(skill for skill in job["parsed"].get("required_skills", []) if skill.lower() in candidate_skills)
            missing = sorted(skill for skill in job["parsed"].get("required_skills", []) if skill.lower() not in candidate_skills)
            skill_score_norm = (len(matched) / len(required_skills)) if required_skills else 0.7

            candidate_years = float(parsed_resume.get("years_experience", 0.0))
            if required_years <= 0:
                experience_score_norm = 0.75
            elif candidate_years >= required_years:
                experience_score_norm = 1.0
            else:
                experience_score_norm = max(0.0, min(1.0, candidate_years / required_years))

            semantic_score_norm = normalize_similarity(float(semantic_scores[index]))
            final_score_norm = (
                (0.5 * skill_score_norm)
                + (0.3 * semantic_score_norm)
                + (0.2 * experience_score_norm)
            )
            skill_score = round(skill_score_norm * 100, 2)
            semantic_score = round(semantic_score_norm * 100, 2)
            experience_score = round(experience_score_norm * 100, 2)
            total = round(final_score_norm * 100, 2)

            computations.append(
                MatchComputation(
                    score=total,
                    semantic_score=round(semantic_score, 2),
                    skill_score=round(skill_score, 2),
                    experience_score=round(experience_score, 2),
                    matched_skills=matched,
                    missing_skills=missing,
                )
            )

        return provider.name, computations

    def debug_score(self, job: dict, resume: dict) -> MatchComputation:
        _, computations = self.score_candidates(job, [{"parsed": resume}])
        return computations[0]


def build_job_embedding_text(job: dict) -> str:
    parsed = job["parsed"]
    return (
        f"Job title: {job['title']}\n"
        f"Required skills: {', '.join(parsed.get('required_skills', []))}\n"
        f"Required experience: {parsed.get('years_experience_required', {}).get('label', '')}\n"
        f"Education: {parsed.get('education', '')}\n"
        f"Responsibilities: {'; '.join(parsed.get('responsibilities', []))}\n"
        f"Full description: {parsed.get('raw_jd', '')}"
    )


def build_resume_embedding_text(parsed_resume: dict) -> str:
    return (
        f"Candidate: {parsed_resume.get('name', '')}\n"
        f"Summary: {parsed_resume.get('summary', '')}\n"
        f"Skills: {', '.join(parsed_resume.get('skills', []))}\n"
        f"Experience: {parsed_resume.get('work_experience', '')}\n"
        f"Education: {parsed_resume.get('education', '')}\n"
        f"Certifications: {', '.join(parsed_resume.get('certifications', []))}"
    )
