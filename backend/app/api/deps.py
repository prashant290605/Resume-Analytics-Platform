from __future__ import annotations

from backend.app.core.config import Settings, get_settings
from backend.app.db.database import Database
from backend.app.db.repository import ScreeningRepository
from backend.app.services.embeddings import MatchingEngine
from backend.app.services.screening import ScreeningService
from fastapi import Request


def get_app_settings() -> Settings:
    return get_settings()


def get_database(request: Request) -> Database:
    return request.app.state.database


def get_repository(request: Request) -> ScreeningRepository:
    return request.app.state.repository


def get_matching_engine(request: Request) -> MatchingEngine:
    return request.app.state.matching_engine


def get_screening_service(request: Request) -> ScreeningService:
    return request.app.state.screening_service
