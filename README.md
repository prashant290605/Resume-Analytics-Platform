# Resume Analytics Platform

Resume Analytics Platform is a production-style hiring application for uploading job descriptions, parsing real PDF resumes, ranking candidates, shortlisting top matches, and generating interview-ready outreach drafts.

## Chosen Product Name

`Resume Analytics Platform`

It is the strongest fit here because it sounds credible for recruiters, covers parsing plus scoring plus analytics, and feels broader and more professional than an internal-tool or demo label.

## Ollama Decision

Ollama remains the primary embedding engine.

It was **not fully replaced** because the alternatives available under a `pip install -r requirements.txt` flow could not be guaranteed to match Ollama on both latency/throughput and resume-matching quality without additional model setup or runtime downloads. To improve usability, the backend now:

- automatically uses Ollama when a local Ollama server is available
- falls back to a built-in TF-IDF embedding path when Ollama is unavailable
- exposes the active provider in dashboard metrics and API health checks

## Final Structure

```text
backend/
  app/
    api/
    core/
    db/
    models/
    services/
    main.py
  data/
    uploads/
  requirements.txt
frontend/
  src/
    components/
    lib/
    pages/
    styles/
  index.html
  package.json
  postcss.config.js
  tailwind.config.js
  vite.config.js
requirements.txt
README.md
```

## Backend

FastAPI handles:

- job description upload by text or file
- multi-file PDF resume upload
- resume parsing into structured candidate data
- hybrid scoring with semantic similarity, skill overlap, and experience fit
- shortlisting
- interview email draft generation
- dashboard metrics and candidate detail APIs

### Run Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

API base URL:

```text
http://127.0.0.1:8000/api
```

## Frontend

React + Vite + Tailwind provides:

- SaaS-style dashboard metrics
- drag-and-drop resume upload
- job intake form with text or file support
- screening controls with progress messaging
- sortable and filterable results table
- full candidate detail view with parsed resume and match breakdown

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Example Workflow

1. Start the FastAPI backend.
2. Start the React frontend.
3. Upload or paste a job description.
4. Upload one or many PDF resumes.
5. Click `Run Screening`.
6. Review ranked candidates on the dashboard.
7. Open a candidate detail page to inspect parsed resume data, matched skills, missing skills, and the generated interview email draft.

## Key API Endpoints

- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/jobs`
- `POST /api/jobs`
- `POST /api/resumes`
- `POST /api/screenings/run`
- `GET /api/results`
- `GET /api/candidates/{resume_id}?screening_id={id}`
