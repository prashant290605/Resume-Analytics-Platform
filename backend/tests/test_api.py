from __future__ import annotations

from backend.tests.conftest import JOB_DESCRIPTION


def _upload_job(client) -> int:
    response = client.post("/api/jobs", data={"title": "Backend Engineer", "description": JOB_DESCRIPTION})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def _upload_resume(client, sample_resume_pdf) -> int:
    with sample_resume_pdf.open("rb") as fh:
        response = client.post("/api/resumes", files=[("files", ("alex.pdf", fh, "application/pdf"))])
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["total_uploaded"] == 1
    return payload["uploaded"][0]["id"]


class TestHealthAndDocs:
    def test_health_reports_provider(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["embedding_provider"] in {"ollama", "local_tfidf"}

    def test_response_time_header_present(self, client):
        assert "x-response-time-ms" in client.get("/api/health").headers

    def test_metrics_endpoint_exposed(self, client):
        assert client.get("/metrics").status_code == 200


class TestUploadValidation:
    def test_rejects_non_pdf_extension(self, client):
        response = client.post("/api/resumes", files=[("files", ("resume.txt", b"hello", "text/plain"))])
        assert response.status_code == 400

    def test_rejects_fake_pdf_content(self, client):
        response = client.post("/api/resumes", files=[("files", ("resume.pdf", b"MZ\x90\x00 not a pdf", "application/pdf"))])
        assert response.status_code == 400

    def test_rejects_oversized_upload(self, client, settings, monkeypatch):
        big = b"%PDF-" + b"0" * (settings.max_upload_bytes + 10)
        response = client.post("/api/resumes", files=[("files", ("resume.pdf", big, "application/pdf"))])
        assert response.status_code == 413

    def test_rejects_short_job_description(self, client):
        response = client.post("/api/jobs", data={"title": "X", "description": "too short"})
        assert response.status_code == 400


class TestScreeningWorkflow:
    def test_full_workflow_upload_screen_results(self, client, sample_resume_pdf):
        job_id = _upload_job(client)
        resume_id = _upload_resume(client, sample_resume_pdf)

        run = client.post("/api/screenings/run", json={"job_id": job_id, "generate_emails": True})
        assert run.status_code == 201, run.text
        screening = run.json()
        assert screening["total_candidates"] == 1

        results = client.get("/api/results", params={"screening_id": screening["screening_id"]})
        assert results.status_code == 200
        candidates = results.json()["candidates"]
        assert len(candidates) == 1
        assert 0.0 <= candidates[0]["score"] <= 100.0

        detail = client.get(
            f"/api/candidates/{resume_id}", params={"screening_id": screening["screening_id"]}
        )
        assert detail.status_code == 200

    def test_screening_without_resumes_fails_cleanly(self, client):
        job_id = _upload_job(client)
        response = client.post("/api/screenings/run", json={"job_id": job_id, "generate_emails": False})
        assert response.status_code == 400

    def test_screening_unknown_job_returns_404(self, client):
        response = client.post("/api/screenings/run", json={"job_id": 999, "generate_emails": False})
        assert response.status_code == 404

    def test_batch_workflow(self, client, sample_resume_pdf):
        batch = client.post("/api/batch/create", json={"name": "July Drive"})
        assert batch.status_code == 201
        batch_id = batch.json()["id"]

        with sample_resume_pdf.open("rb") as fh:
            upload = client.post(
                f"/api/batch/{batch_id}/upload", files=[("files", ("alex.pdf", fh, "application/pdf"))]
            )
        assert upload.status_code == 201
        assert upload.json()["uploaded"][0]["batch_id"] == batch_id

    def test_upload_to_missing_batch_returns_404(self, client, sample_resume_pdf):
        with sample_resume_pdf.open("rb") as fh:
            response = client.post("/api/batch/999/upload", files=[("files", ("alex.pdf", fh, "application/pdf"))])
        assert response.status_code == 404


class TestDashboard:
    def test_dashboard_counts_update(self, client, sample_resume_pdf):
        before = client.get("/api/dashboard").json()["total_resumes"]
        _upload_resume(client, sample_resume_pdf)
        after = client.get("/api/dashboard").json()["total_resumes"]
        assert after == before + 1
