from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.config import get_settings
from app.services.history_service import HistoryService
from app.services.query_service import QueryService


router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
def list_history() -> list[dict[str, object]]:
    settings = get_settings()
    history_service = HistoryService(QueryService(settings.resolved_app_database_url))
    return history_service.list_sessions()


@router.get("/history/{session_id}")
def get_history(session_id: UUID) -> dict[str, object]:
    settings = get_settings()
    history_service = HistoryService(QueryService(settings.resolved_app_database_url))
    session = history_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
