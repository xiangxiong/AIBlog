from __future__ import annotations

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
INIT_DIR = ROOT_DIR / "db" / "init"


def load_database_url() -> str:
    load_dotenv(ROOT_DIR / ".env")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required. Copy .env.example to .env first.")
    return database_url


def execute_file(conn: psycopg.Connection, path: Path) -> None:
    print(f"Running {path.name}...")
    conn.execute(path.read_text(encoding="utf-8"))


def main() -> None:
    database_url = load_database_url()
    sql_files = [
        INIT_DIR / "001_schema.sql",
        INIT_DIR / "002_seed_data.sql",
    ]

    with psycopg.connect(database_url, autocommit=True) as conn:
        for sql_file in sql_files:
            execute_file(conn, sql_file)

    print("PostgreSQL demo database reset complete.")


if __name__ == "__main__":
    main()
