from __future__ import annotations

from app.models import ChartConfig, QueryResult


TIME_WORDS = ("date", "time", "month", "day", "week", "year", "ordered_at", "paid_at")
NUMERIC_WORDS = ("amount", "total", "count", "sum", "avg", "gmv", "profit", "rate", "price")


class ChartService:
    def recommend(self, result: QueryResult) -> ChartConfig | None:
        if len(result.columns) < 2 or result.row_count == 0:
            return None

        x_column = result.columns[0]
        y_column = self._find_numeric_column(result)
        if not y_column:
            return None

        if self._looks_like_time(x_column):
            return ChartConfig(type="line", x=x_column, y=y_column, reason="时间字段加数值字段，适合趋势折线图。")

        if result.row_count <= 8 and "rate" in y_column.lower():
            return ChartConfig(type="pie", x=x_column, y=y_column, reason="少量分类占比指标，适合饼图。")

        return ChartConfig(type="bar", x=x_column, y=y_column, reason="分类字段加数值字段，适合柱状图。")

    def _find_numeric_column(self, result: QueryResult) -> str | None:
        for column_index, column in enumerate(result.columns):
            if self._looks_numeric(result.rows, column_index) or any(word in column.lower() for word in NUMERIC_WORDS):
                return column
        return None

    def _looks_numeric(self, rows: list[list[object]], column_index: int) -> bool:
        values = [row[column_index] for row in rows if row[column_index] is not None]
        return bool(values) and all(isinstance(value, (int, float)) for value in values)

    def _looks_like_time(self, column: str) -> bool:
        lower = column.lower()
        return any(word in lower for word in TIME_WORDS)
