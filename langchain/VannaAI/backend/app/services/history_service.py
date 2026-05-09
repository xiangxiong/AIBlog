from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from app.services.query_service import QueryService


class HistoryService:
    def __init__(self, query_service: QueryService) -> None:
        self.query_service = query_service

    def ensure_session(self, session_id: UUID | None, title: str) -> UUID:
        if session_id:
            rows = self.query_service.fetch_all(
                "SELECT id FROM chat_sessions WHERE id = %s",
                (session_id,),
            )
            if rows:
                return session_id

        new_session_id = uuid4()
        self.query_service.execute(
            """
            INSERT INTO chat_sessions (id, title)
            VALUES (%s, %s)
            """,
            (new_session_id, title[:80]),
        )
        return new_session_id

    def add_message(self, session_id: UUID, role: str, content: str) -> None:
        self.query_service.execute(
            """
            INSERT INTO chat_messages (id, session_id, role, content)
            VALUES (%s, %s, %s, %s)
            """,
            (uuid4(), session_id, role, content),
        )
        self.query_service.execute(
            "UPDATE chat_sessions SET updated_at = NOW() WHERE id = %s",
            (session_id,),
        )

    def add_query_log(
        self,
        session_id: UUID,
        question: str,
        generated_sql: str | None,
        status: str,
        error_message: str | None,
        row_count: int,
        execution_ms: int,
    ) -> None:
        self.query_service.execute(
            """
            INSERT INTO query_logs (
                id, session_id, question, generated_sql, status,
                error_message, row_count, execution_ms
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                uuid4(),
                session_id,
                question,
                generated_sql,
                status,
                error_message,
                row_count,
                execution_ms,
            ),
        )

    def list_sessions(self) -> list[dict[str, Any]]:
        return self.query_service.fetch_all(
            """
            SELECT id, title, created_at, updated_at
            FROM chat_sessions
            ORDER BY updated_at DESC
            LIMIT 50
            """
        )

    def get_session(self, session_id: UUID) -> dict[str, Any] | None:
        sessions = self.query_service.fetch_all(
            "SELECT id, title FROM chat_sessions WHERE id = %s",
            (session_id,),
        )
        if not sessions:
            return None

        messages = self.query_service.fetch_all(
            """
            SELECT id, role, content, created_at
            FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,),
        )
        query_logs = self.query_service.fetch_all(
            """
            SELECT id, question, generated_sql, status, error_message, row_count, execution_ms, created_at
            FROM query_logs
            WHERE session_id = %s
            ORDER BY created_at DESC
            """,
            (session_id,),
        )

        return {
            "id": sessions[0]["id"],
            "title": sessions[0]["title"],
            "messages": messages,
            "query_logs": query_logs,
        }
