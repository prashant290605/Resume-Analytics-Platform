from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.app.core.config import DEFAULT_SHORTLIST_THRESHOLD, JOB_UPLOAD_DIR, RESUME_UPLOAD_DIR
from backend.app.data.default_jds import DEFAULT_JOB_DESCRIPTIONS
from backend.app.db.database import Database
from backend.app.db.repository import ScreeningRepository
from backend.app.models.schemas import (
    BatchCreateRequest,
    BatchResponse,
    CandidateDetailResponse,
    DashboardMetrics,
    DefaultJDResponse,
    HealthResponse,
    JobDescriptionResponse,
    ResumeUploadItem,
    ResumeUploadResponse,
    ResultsResponse,
    RunScreeningRequest,
    ScreeningRunResponse,
)
from backend.app.services.embeddings import MatchingEngine
from backend.app.services.parsing import extract_text_from_pdf, parse_job_description, parse_resume_text
from backend.app.services.screening import ScreeningService

router = APIRouter(prefix="/api")
database = Database()
repository = ScreeningRepository(database)
screening_service = ScreeningService(repository)
matching_engine = MatchingEngine()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", embedding_provider=matching_engine.active_provider().name)


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard() -> DashboardMetrics:
    return DashboardMetrics(**repository.dashboard_metrics())


@router.get("/jobs", response_model=list[JobDescriptionResponse])
async def list_jobs() -> list[JobDescriptionResponse]:
    return [JobDescriptionResponse(**job) for job in repository.list_jobs()]


@router.get("/default-jds", response_model=list[DefaultJDResponse])
async def get_default_job_descriptions() -> list[DefaultJDResponse]:
    return [DefaultJDResponse(**item) for item in DEFAULT_JOB_DESCRIPTIONS]


@router.post("/batch/create", response_model=BatchResponse)
async def create_batch(request: BatchCreateRequest) -> BatchResponse:
    batch = repository.create_batch(request.name.strip() or "Hiring Batch")
    return BatchResponse(**batch)


@router.post("/jobs", response_model=JobDescriptionResponse)
async def upload_job_description(
    title: str = Form(...),
    description: str = Form(""),
    file: UploadFile | None = File(default=None),
) -> JobDescriptionResponse:
    source_type = "text"
    raw_text = description.strip()
    file_name = None
    file_path = None

    if file is not None:
        source_type = "file"
        destination = JOB_UPLOAD_DIR / file.filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_name = file.filename
        file_path = str(destination)
        suffix = Path(file.filename).suffix.lower()
        raw_text = extract_text_from_pdf(destination) if suffix == ".pdf" else destination.read_text(encoding="utf-8", errors="ignore")

    if len(raw_text) < 20:
        raise HTTPException(status_code=400, detail="Provide a meaningful job description as text or file.")

    job = repository.create_job(
        title=title.strip(),
        source_type=source_type,
        raw_text=raw_text,
        parsed=parse_job_description(title=title.strip(), description=raw_text),
        file_name=file_name,
        file_path=file_path,
    )
    return JobDescriptionResponse(**job)


@router.post("/resumes", response_model=ResumeUploadResponse)
async def upload_resumes(files: list[UploadFile] = File(...)) -> ResumeUploadResponse:
    return await upload_resumes_to_batch(batch_id=None, files=files)


@router.post("/batch/{batch_id}/upload", response_model=ResumeUploadResponse)
async def upload_resumes_to_batch(batch_id: int | None, files: list[UploadFile] = File(...)) -> ResumeUploadResponse:
    if batch_id is not None and not repository.get_batch(batch_id):
        raise HTTPException(status_code=404, detail="Batch not found.")

    uploaded: list[ResumeUploadItem] = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF resume.")

        destination = unique_upload_destination(RESUME_UPLOAD_DIR, file.filename, batch_id=batch_id)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        parsed = parse_resume_text(extract_text_from_pdf(destination), file.filename)
        resume = repository.create_resume(file_name=file.filename, file_path=str(destination), parsed=parsed, batch_id=batch_id)
        uploaded.append(
            ResumeUploadItem(
                id=resume["id"],
                batch_id=resume.get("batch_id"),
                file_name=resume["file_name"],
                candidate_name=resume["parsed"].get("name", "Unknown Candidate"),
                email=resume["parsed"].get("email"),
                skills=resume["parsed"].get("skills", []),
            )
        )

    return ResumeUploadResponse(uploaded=uploaded, total_uploaded=len(uploaded))


@router.post("/screenings/run", response_model=ScreeningRunResponse)
async def run_screening(request: RunScreeningRequest) -> ScreeningRunResponse:
    payload = screening_service.run_screening(
        job_id=request.job_id,
        batch_id=request.batch_id,
        threshold=request.threshold if request.threshold is not None else DEFAULT_SHORTLIST_THRESHOLD,
        generate_emails=request.generate_emails,
    )
    return ScreeningRunResponse(**payload)


@router.get("/results", response_model=ResultsResponse)
async def get_results(screening_id: int | None = None) -> ResultsResponse:
    return ResultsResponse(**screening_service.get_results(screening_id=screening_id))


@router.get("/batch/{batch_id}/results", response_model=ResultsResponse)
async def get_batch_results(batch_id: int) -> ResultsResponse:
    batch_results = repository.get_batch_results(batch_id)
    if not batch_results:
        return ResultsResponse(
            screening_id=None,
            job_id=None,
            batch_id=batch_id,
            job_title=None,
            threshold=None,
            embedding_provider=None,
            candidates=[],
        )

    return ResultsResponse(**screening_service.get_results(screening_id=batch_results["screening"]["id"]))


@router.get("/candidates/{resume_id}", response_model=CandidateDetailResponse)
async def get_candidate_detail(resume_id: int, screening_id: int) -> CandidateDetailResponse:
    return CandidateDetailResponse(**screening_service.get_candidate_detail(screening_id=screening_id, resume_id=resume_id))


def unique_upload_destination(base_dir: Path, original_name: str, batch_id: int | None) -> Path:
    suffix = Path(original_name).suffix
    stem = Path(original_name).stem
    batch_prefix = f"batch_{batch_id}_" if batch_id is not None else ""
    counter = 0

    while True:
        candidate_name = f"{batch_prefix}{stem}{'' if counter == 0 else f'_{counter}'}{suffix}"
        destination = base_dir / candidate_name
        if not destination.exists():
            return destination
        counter += 1
