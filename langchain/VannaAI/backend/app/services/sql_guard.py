from __future__ import annotations

import re


FORBIDDEN_KEYWORDS = {
    "alter",
    "create",
    "delete",
    "drop",
    "execute",
    "grant",
    "insert",
    "merge",
    "revoke",
    "truncate",
    "update",
}


class SqlGuard:
    def __init__(self, row_limit: int = 200) -> None:
        self.row_limit = row_limit

    def validate(self, sql: str) -> str:
        cleaned = self._clean(sql)
        normalized = cleaned.lower()

        if ";" in cleaned.rstrip(";"):
            raise ValueError("Only one SQL statement is allowed.")

        normalized = normalized.rstrip(";").strip()
        if not normalized.startswith(("select", "with")):
            raise ValueError("Only SELECT/WITH queries are allowed.")

        tokens = set(re.findall(r"\b[a-z_]+\b", normalized))
        blocked = sorted(tokens & FORBIDDEN_KEYWORDS)
        if blocked:
            raise ValueError(f"Unsafe SQL keyword detected: {', '.join(blocked)}")

        return self._apply_limit(cleaned.rstrip(";").strip())

    def _clean(self, sql: str) -> str:
        sql = sql.strip()
        sql = re.sub(r"^```(?:sql)?", "", sql, flags=re.IGNORECASE).strip()
        sql = re.sub(r"```$", "", sql).strip()
        sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
        sql = re.sub(r"--.*?$", " ", sql, flags=re.MULTILINE)
        return sql.strip()

    def _apply_limit(self, sql: str) -> str:
        if re.search(r"\blimit\s+\d+\b", sql, flags=re.IGNORECASE):
            return sql
        return f"SELECT * FROM ({sql}) AS vanna_result LIMIT {self.row_limit}"
