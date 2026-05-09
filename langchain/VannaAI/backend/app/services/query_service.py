from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from time import perf_counter
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.models import QueryResult


class QueryService:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def fetch_query_result(self, sql: str) -> QueryResult:
        started_at = perf_counter()
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SET TRANSACTION READ ONLY")
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [column.name for column in cursor.description or []]

        execution_ms = int((perf_counter() - started_at) * 1000)
        serialized_rows = [
            [self._serialize_value(row[column]) for column in columns]
            for row in rows
        ]
        return QueryResult(
            columns=columns,
            rows=serialized_rows,
            row_count=len(serialized_rows),
            execution_ms=execution_ms,
        )

    def fetch_all(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value
