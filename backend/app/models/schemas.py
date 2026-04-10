from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    embedding_provider: str


class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    source_type: Literal["text", "file"]
    parsed: dict[str, Any]
    created_at: str


class DefaultJDResponse(BaseModel):
    id: str
    title: str
    experience: str
    keywords: list[str]
    required_skills: list[str]
    description: str


class ResumeUploadItem(BaseModel):
    id: int
    batch_id: int | None = None
    file_name: str
    candidate_name: str
    email: str | None = None
    skills: list[str] = Field(default_factory=list)


class ResumeUploadResponse(BaseModel):
    uploaded: list[ResumeUploadItem]
    total_uploaded: int


class RunScreeningRequest(BaseModel):
    job_id: int
    batch_id: int | None = None
    threshold: float = Field(default=70.0, ge=0, le=100)
    generate_emails: bool = True


class BatchCreateRequest(BaseModel):
    name: str = Field(default="Hiring Batch")


class BatchResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: str


class CandidateSummary(BaseModel):
    resume_id: int
    screening_id: int
    name: str
    email: str | None = None
    score: float
    semantic_score: float
    skill_score: float
    experience_score: float
    skills: list[str]
    years_experience: float
    shortlisted: bool
    matched_skills: list[str]
    missing_skills: list[str]
    job_title: str


class ScreeningRunResponse(BaseModel):
    screening_id: int
    job_id: int
    batch_id: int | None = None
    job_title: str
    total_candidates: int
    shortlisted_count: int
    average_score: float
    embedding_provider: str
    candidates: list[CandidateSummary]


class DashboardMetrics(BaseModel):
    total_resumes: int
    shortlisted_candidates: int
    average_match_score: float
    screenings_run: int
    latest_job_title: str | None = None
    latest_screening_id: int | None = None
    embedding_provider: str


class ResultsResponse(BaseModel):
    screening_id: int | None
    job_id: int | None
    batch_id: int | None = None
    job_title: str | None
    threshold: float | None
    embedding_provider: str | None
    candidates: list[CandidateSummary]


class CandidateDetailResponse(BaseModel):
    resume_id: int
    screening_id: int
    job_title: str
    score: float
    shortlisted: bool
    parsed_resume: dict[str, Any]
    match_breakdown: dict[str, Any]
    generated_email: str | None = None
