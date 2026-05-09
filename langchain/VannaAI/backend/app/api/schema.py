from __future__ import annotations
from fastapi import APIRouter
from app.config import get_settings
from app.services.query_service import QueryService
from app.services.schema_service import SchemaService


router = APIRouter(prefix="/api", tags=["schema"])


@router.get("/schema")
def get_schema() -> dict[str, object]:
    settings = get_settings()
    query_service = QueryService(settings.database_url)
    schema_service = SchemaService(query_service, settings.business_tables)
    return {
        "tables": settings.business_tables,
        "columns": schema_service.list_columns(),
        "foreign_keys": schema_service.list_foreign_keys(),
        "prompt_context": schema_service.build_prompt_context(),
    }
