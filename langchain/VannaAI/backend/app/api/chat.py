from __future__ import annotations
from fastapi import APIRouter
from app.config import get_settings
from app.models import ChatRequest, ChatResponse
from app.services.chart_service import ChartService
from app.services.history_service import HistoryService
from app.services.query_service import QueryService
from app.services.schema_service import SchemaService
from app.services.sql_guard import SqlGuard
from app.services.vanna_service import VannaService


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    settings = get_settings()
    business_query_service = QueryService(settings.database_url)
    app_query_service = QueryService(settings.resolved_app_database_url)
    history_service = HistoryService(app_query_service)
    session_id = history_service.ensure_session(request.session_id, request.question)
    history_service.add_message(session_id, "user", request.question)

    generated_sql: str | None = None
    try:
        schema_service = SchemaService(business_query_service, settings.business_tables)
        schema_context = schema_service.build_prompt_context()
        generated_sql = await VannaService(settings.llm_config).generate_sql(
            question=request.question,
            schema_context=schema_context,
        )

        guarded_sql = SqlGuard(settings.query_row_limit).validate(generated_sql)
        result = business_query_service.fetch_query_result(guarded_sql)
        chart = ChartService().recommend(result)

        summary = None
        if request.include_summary:
            summary = await VannaService(settings.llm_config).summarize(
                question=request.question,
                sql=guarded_sql,
                result=result,
            )

        assistant_content = summary or f"SQL executed successfully. Rows: {result.row_count}"
        history_service.add_message(session_id, "assistant", assistant_content)
        history_service.add_query_log(
            session_id=session_id,
            question=request.question,
            generated_sql=guarded_sql,
            status="success",
            error_message=None,
            row_count=result.row_count,
            execution_ms=result.execution_ms,
        )

        return ChatResponse(
            session_id=session_id,
            question=request.question,
            sql=guarded_sql if request.show_sql else None,
            columns=result.columns,
            rows=result.rows,
            row_count=result.row_count,
            execution_ms=result.execution_ms,
            chart=chart,
            summary=summary,
            error=None,
        )
    except Exception as exc:
        error_message = str(exc)
        history_service.add_message(session_id, "assistant", error_message)
        history_service.add_query_log(
            session_id=session_id,
            question=request.question,
            generated_sql=generated_sql,
            status="error",
            error_message=error_message,
            row_count=0,
            execution_ms=0,
        )
        return ChatResponse(
            session_id=session_id,
            question=request.question,
            sql=generated_sql if request.show_sql else None,
            columns=[],
            rows=[],
            row_count=0,
            execution_ms=0,
            chart=None,
            summary=None,
            error=error_message,
        )
