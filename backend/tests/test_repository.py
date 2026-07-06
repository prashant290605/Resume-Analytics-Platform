from __future__ import annotations

PARSED_RESUME = {
    "name": "Alex Candidate",
    "email": "alex@example.com",
    "summary": "Backend engineer.",
    "skills": ["Python", "SQL"],
    "work_experience": "4 years.",
    "education": "B.E.",
    "certifications": [],
    "years_experience": 4,
}

PARSED_JOB = {
    "required_skills": ["Python", "SQL"],
    "years_experience_required": {"minimum": 2, "label": "2 years"},
    "education": "Bachelor",
    "responsibilities": ["Build APIs"],
    "raw_jd": "Backend engineer role using Python and SQL.",
}


class TestRepository:
    def test_create_and_get_job(self, repository):
        job = repository.create_job(
            title="Backend Engineer", source_type="text",
            raw_text=PARSED_JOB["raw_jd"], parsed=PARSED_JOB,
            file_name=None, file_path=None,
        )
        fetched = repository.get_job(job["id"])
        assert fetched is not None
        assert fetched["title"] == "Backend Engineer"
        assert fetched["parsed"]["required_skills"] == ["Python", "SQL"]

    def test_create_resume_within_batch(self, repository):
        batch = repository.create_batch("July Batch")
        resume = repository.create_resume("a.pdf", "/tmp/a.pdf", PARSED_RESUME, batch_id=batch["id"])
        in_batch = repository.list_resumes(batch_id=batch["id"])
        all_resumes = repository.list_resumes()
        assert len(in_batch) == 1
        assert in_batch[0]["id"] == resume["id"]
        assert len(all_resumes) == 1

    def test_screening_with_matches_roundtrip(self, repository):
        job = repository.create_job(
            title="Backend Engineer", source_type="text",
            raw_text=PARSED_JOB["raw_jd"], parsed=PARSED_JOB,
            file_name=None, file_path=None,
        )
        resume = repository.create_resume("a.pdf", "/tmp/a.pdf", PARSED_RESUME)
        screening_id = repository.create_screening(job["id"], threshold=70.0, embedding_provider="local_tfidf")
        repository.add_match(
            screening_id=screening_id, resume_id=resume["id"],
            score=88.0, semantic_score=80.0, skill_score=100.0, experience_score=90.0,
            shortlisted=True,
            breakdown={"matched_skills": ["Python", "SQL"], "missing_skills": []},
            generated_email=None,
        )
        matches = repository.list_matches(screening_id)
        assert len(matches) == 1
        assert matches[0]["score"] == 88.0
        assert matches[0]["shortlisted"]

    def test_dashboard_metrics_counts(self, repository):
        assert repository.dashboard_metrics()["total_resumes"] == 0
        repository.create_resume("a.pdf", "/tmp/a.pdf", PARSED_RESUME)
        assert repository.dashboard_metrics()["total_resumes"] == 1
