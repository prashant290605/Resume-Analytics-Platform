# Architecture

## Overview

The platform is a layered FastAPI application with a React SPA. The backend owns all business logic; the frontend is a thin client over the REST API.

## Layers

**api/** — HTTP concerns only: routing, request validation, response shaping. Upload validation happens here (extension check, `%PDF` magic bytes, size cap → 400/413) before anything touches disk. Handlers receive dependencies via `Depends`; none construct their own collaborators.

**services/** — Domain logic:
- `parsing.py` extracts text from PDFs (PyMuPDF) and derives structured candidate/JD data (skills, experience, education, contacts) via keyword + section heuristics.
- `embeddings.py` defines the `EmbeddingProvider` Protocol and the `MatchingEngine`, which combines semantic similarity with skill-overlap and experience-fit scores into a single 0–100 score with a persisted breakdown.
- `screening.py` orchestrates a run: load JD + resumes → score → persist screening + matches → optionally generate outreach emails.

**db/** — `Database` (connection lifecycle, schema, WAL mode, indexes) and `ScreeningRepository` (all SQL, parametrized). No other module writes SQL.

**core/** — `Settings` (pydantic-settings, `RAP_` env prefix) and logging configuration.

## Dependency injection

`main.py` is the composition root. The FastAPI lifespan builds the object graph once:

```
Database → ScreeningRepository → ScreeningService ← MatchingEngine
```

stored on `app.state` and exposed through provider functions in `api/deps.py`. Tests build the same graph against a temp directory — no monkeypatching of module globals.

## Embedding provider fallback

`MatchingEngine` probes Ollama (`/api/tags`, 1.5 s timeout) per screening run:

- **Available** → `nomic-embed-text` embeddings (higher semantic quality).
- **Unavailable** → deterministic TF-IDF + cosine similarity (zero dependencies, reproducible tests, sub-second at 200 resumes).

The active provider is recorded on each screening row, so results are auditable.

## Scoring model

```
score = 0.45 · skill_overlap + 0.35 · semantic_similarity + 0.20 · experience_fit   (see embeddings.py for exact weights)
```

Skill overlap uses canonicalized keyword matching between JD-required skills and resume skills; experience fit compares extracted years against the JD minimum. Matched/missing skills are persisted per candidate for explainability in the UI.

## Storage: why SQLite

Single-tenant deployment, embedded zero-ops persistence, WAL mode for concurrent reads, covering indexes on `matches(screening_id)`, `resumes(batch_id)`, `screenings(job_id/batch_id)`. The repository pattern contains a future Postgres migration to a single module; that migration is deliberately deferred until multi-tenant or concurrent-writer requirements exist.

## Observability

- Access-log middleware records method, path, status, latency; latency is also returned as `X-Response-Time-Ms`.
- `prometheus-fastapi-instrumentator` exposes request histograms at `/metrics`.
- Global exception handler logs stack traces server-side and returns an opaque 500 envelope.

## Failure modes considered

| Failure | Behaviour |
|---|---|
| Ollama down | Automatic TF-IDF fallback, provider recorded |
| Malformed/renamed PDF | Rejected by magic-byte check (400) |
| Oversized upload | Rejected before write (413) |
| Duplicate filenames | Collision-safe unique destination naming |
| Unhandled exception | Logged with trace; client gets opaque 500 |
