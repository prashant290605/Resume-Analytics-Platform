# Deployment

**Live instance:** https://resume-analytics-i93z.onrender.com (Render free tier; cold-starts after idle).

## Local (Docker Compose)

```bash
docker compose up --build
# frontend http://localhost:3000 · API http://localhost:8000/docs
```

Data persists in the `rap-data` volume. Optional Ollama: `docker compose --profile ollama up --build` and set `RAP_OLLAMA_BASE_URL=http://ollama:11434` on the backend service.

## Render (free tier)

1. Push this repo to GitHub.
2. Render → New → Web Service → connect the repo.
3. Environment: **Docker**; Dockerfile path: `backend/Dockerfile`; context: repo root.
4. Add a Disk (1 GB) mounted at `/data` (SQLite + uploads live there via `RAP_DATA_DIR=/data`).
5. Set env vars: `RAP_CORS_ORIGINS=["https://<your-frontend-url>"]`.
6. Create a second service (Static Site) for the frontend: build command `npm ci && npm run build` in `frontend/`, publish dir `frontend/dist`, env `VITE_API_URL=https://<backend-url>/api`.

## Railway

Same shape: two services from one repo (backend Dockerfile + frontend static build), volume mounted at `/data`.

## Checklist before sharing the URL

- [ ] `/api/health` returns `{"status":"ok", ...}`
- [ ] Upload a sample from `samples/`, run a screening, view results
- [ ] Put the live URL at the top of README.md and in the resume PDF link
