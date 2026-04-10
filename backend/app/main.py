from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router


app = FastAPI(
    title="Resume Analytics Platform",
    version="1.0.0",
    description="Production-ready API for resume ingestion, scoring, shortlisting, and interview email generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Resume Analytics Platform API"}
