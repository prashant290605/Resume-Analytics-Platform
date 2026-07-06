from __future__ import annotations

from backend.app.services.parsing import extract_text_from_pdf, parse_job_description, parse_resume_text
from backend.tests.conftest import JOB_DESCRIPTION


class TestResumeParsing:
    def test_extracts_text_from_pdf(self, sample_resume_pdf):
        text = extract_text_from_pdf(sample_resume_pdf)
        assert "Alex Candidate" in text
        assert "FastAPI" in text

    def test_parses_contact_and_skills(self, sample_resume_pdf):
        parsed = parse_resume_text(extract_text_from_pdf(sample_resume_pdf), sample_resume_pdf.name)
        assert parsed["email"] == "alex.candidate@example.com"
        assert "Python" in parsed["skills"]
        assert "FastAPI" in parsed["skills"]

    def test_extracts_years_of_experience(self, sample_resume_pdf):
        parsed = parse_resume_text(extract_text_from_pdf(sample_resume_pdf), sample_resume_pdf.name)
        assert parsed["years_experience"] >= 3


class TestJobParsing:
    def test_parses_required_skills(self):
        parsed = parse_job_description(title="Backend Engineer", description=JOB_DESCRIPTION)
        assert "Python" in parsed["required_skills"]
        assert "Docker" in parsed["required_skills"]

    def test_keeps_raw_text(self):
        parsed = parse_job_description(title="Backend Engineer", description=JOB_DESCRIPTION)
        assert parsed["raw_jd"]
