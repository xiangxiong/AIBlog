from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: UUID | None = None
    show_sql: bool = True
    include_summary: bool = True


class ChartConfig(BaseModel):
    type: str
    x: str | None = None
    y: str | None = None
    reason: str


class QueryResult(BaseModel):
    columns: list[str]
    rows: list[list[Any]]
    row_count: int
    execution_ms: int


class ChatResponse(BaseModel):
    session_id: UUID
    question: str
    sql: str | None
    columns: list[str]
    rows: list[list[Any]]
    row_count: int
    execution_ms: int
    chart: ChartConfig | None = None
    summary: str | None = None
    error: str | None = None


class SchemaColumn(BaseModel):
    table_name: str
    column_name: str
    data_type: str
    is_nullable: bool


class HistoryItem(BaseModel):
    id: UUID
    title: str
    created_at: str
    updated_at: str


class HistoryDetail(BaseModel):
    id: UUID
    title: str
    messages: list[dict[str, Any]]
    query_logs: list[dict[str, Any]]
