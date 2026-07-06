# Resume Analytics Platform

[![CI](https://github.com/prashant290605/Resume-Analytics-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/prashant290605/Resume-Analytics-Platform/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-style resume screening platform. Upload job descriptions and PDF resumes; a hybrid scoring engine (semantic similarity + skill overlap + experience fit) ranks candidates, shortlists top matches, and drafts interview outreach emails — behind a typed FastAPI backend with a React dashboard.

**Measured:** parses and ranks a 200-resume batch in **under 1 second** on the deterministic TF-IDF path (see [Benchmarks](#benchmarks)).

## Quickstart

```bash
# Everything (frontend on :3000, API on :8000)
docker compose up --build

# With higher-quality Ollama embeddings
docker compose --profile ollama up --build
```

Manual setup:

```bash
make install          # backend deps
make run              # API on :8000 (docs at /docs)
make frontend         # React dev server on :5173
make test             # pytest suite
```

## Architecture

```text
            ┌─────────────────────┐
            │   React + Tailwind  │  nginx-served SPA, /api proxied
            └──────────┬──────────┘
                       │ REST
            ┌──────────▼──────────┐
            │   FastAPI backend   │  DI composition root (lifespan)
            ├─────────────────────┤
            │ api/      routes + validation (magic bytes, size caps)
            │ services/ parsing · hybrid scoring · screening · email
            │ db/       SQLite repository (WAL, indexed)
            │ core/     env-driven settings · logging
            └──────────┬──────────┘
             ┌─────────▼─────────┐
             │ EmbeddingProvider │  Protocol: Ollama ──fallback──▶ TF-IDF
             └───────────────────┘
```

Key design decisions (full rationale in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)):

- **Pluggable embeddings.** Providers implement a typed `Protocol`; Ollama is probed at runtime with graceful fallback to deterministic TF-IDF, so the system works with zero external dependencies and tests stay reproducible.
- **Hybrid scoring, not just cosine similarity.** Final score = weighted semantic similarity + skill overlap + experience fit, with a per-candidate breakdown persisted for explainability.
- **Dependency injection.** All long-lived objects are built once in the FastAPI lifespan and injected via `Depends` — no import-time singletons, trivially testable.
- **SQLite on purpose.** Single-tenant tool, zero-ops persistence, WAL mode + covering indexes. The repository layer isolates SQL, so a Postgres migration is contained to one module.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health + active embedding provider |
| GET | `/api/dashboard` | Aggregate metrics |
| POST | `/api/jobs` | Upload JD (text or PDF) |
| GET | `/api/jobs` | List JDs |
| POST | `/api/resumes` | Upload resume PDFs (validated) |
| POST | `/api/batch/create` | Create a hiring batch |
| POST | `/api/batch/{id}/upload` | Upload resumes into a batch |
| POST | `/api/screenings/run` | Rank all/batch resumes against a JD |
| GET | `/api/results` | Ranked results with score breakdowns |
| GET | `/api/candidates/{id}` | Candidate detail + generated outreach email |
| GET | `/metrics` | Prometheus metrics |

Interactive docs: `http://localhost:8000/docs`.

## Benchmarks

Measured on the TF-IDF fallback path (no GPU, no external services):

| Operation | Result |
|---|---|
| Parse 200 PDF resumes | 0.61 s |
| Score + rank 200 candidates | 0.07 s |
| End-to-end batch screening | **0.68 s** |

Reproduce: upload `samples/` PDFs (or any set) and time `POST /api/screenings/run`.

## Testing & Quality

- **27 pytest tests**: parsing units, scoring properties (bounds, ordering, disjoint skill sets), repository round-trips on isolated temp DBs, and end-to-end API workflows including upload validation (extension, `%PDF` magic bytes, size caps) and error paths.
- **CI** (GitHub Actions): ruff lint + pytest, frontend build, and Docker image builds on every push.
- **Observability**: structured request logs with latency, `X-Response-Time-Ms` header, Prometheus `/metrics`.

```bash
make test && make lint
```

## Configuration

All settings are env-driven with sane defaults (see [.env.example](.env.example)): `RAP_DATA_DIR`, `RAP_OLLAMA_BASE_URL`, `RAP_OLLAMA_MODEL`, `RAP_DEFAULT_SHORTLIST_THRESHOLD`, `RAP_CORS_ORIGINS`, `RAP_MAX_UPLOAD_BYTES`, `RAP_ENABLE_METRICS`, `RAP_LOG_LEVEL`.

## Project Structure

```text
backend/
  app/
    api/        routes, dependency providers
    core/       settings (pydantic-settings), logging
    data/       built-in sample job descriptions
    db/         SQLite database + repository
    models/     Pydantic request/response schemas
    services/   parsing, embeddings, screening, email generation
  tests/        pytest suite (unit + integration)
  Dockerfile
frontend/       React (Vite) + Tailwind SPA, nginx Dockerfile
samples/        5 sample resumes for demos
docs/           architecture & deployment notes
```

## Deployment

One-command local deploy via Docker Compose; cloud steps for Render/Railway in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Non-Goals (deliberate)

- **No auth/user accounts** — single-tenant recruiter tool; adding auth without a threat model is scope creep. The nginx layer is the place for basic auth if exposed publicly.
- **No task queue** — batch screening completes in <1 s; a queue becomes worthwhile only if parsing moves to LLM-based extraction.

## License

MIT © Prashant Singh
