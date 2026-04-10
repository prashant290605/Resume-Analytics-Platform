import unittest

from backend.app.services.embeddings import MatchingEngine


class ScoringRegressionTest(unittest.TestCase):
    def test_matching_resume_scores_above_seventy(self) -> None:
        engine = MatchingEngine()
        engine.ollama_provider.is_available = lambda: False  # force deterministic fallback

        job = {
            "title": "Backend Engineer",
            "parsed": {
                "required_skills": ["Python", "FastAPI", "SQL", "Docker", "AWS"],
                "years_experience_required": {"minimum": 4, "label": "4 years"},
                "education": "Bachelor",
                "responsibilities": ["Build APIs", "Work with cloud infrastructure"],
                "raw_jd": "Backend Engineer using Python FastAPI SQL Docker AWS building APIs and services.",
            },
        }
        resume = {
            "name": "Alex Candidate",
            "summary": "Backend engineer building Python FastAPI services on AWS with Docker and SQL.",
            "skills": ["Python", "FastAPI", "SQL", "Docker", "AWS"],
            "work_experience": "4 years building Python FastAPI APIs on AWS and Docker.",
            "education": "Bachelor of Engineering",
            "certifications": [],
            "years_experience": 4,
        }

        computation = engine.debug_score(job, resume)
        self.assertGreater(computation.score, 70.0)


if __name__ == "__main__":
    unittest.main()
