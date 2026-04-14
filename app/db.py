import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def get_database_path() -> str:
    return os.getenv("DATABASE_PATH", "/data/dashboard.db")


@contextmanager
def get_connection():
    db_path = Path(get_database_path())
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT DEFAULT '',
                status_enabled INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                content TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT INTO notes (id, content, updated_at)
            VALUES (1, '', ?)
            ON CONFLICT(id) DO NOTHING
            """,
            (utc_now(),),
        )


def list_services() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, url, description, status_enabled, created_at, updated_at
            FROM services
            ORDER BY LOWER(name) ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def create_service(name: str, url: str, description: str, status_enabled: bool) -> None:
    now = utc_now()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO services (name, url, description, status_enabled, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name.strip(), url.strip(), description.strip(), int(status_enabled), now, now),
        )


def update_service(service_id: int, name: str, url: str, description: str, status_enabled: bool) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE services
            SET name = ?, url = ?, description = ?, status_enabled = ?, updated_at = ?
            WHERE id = ?
            """,
            (name.strip(), url.strip(), description.strip(), int(status_enabled), utc_now(), service_id),
        )


def delete_service(service_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM services WHERE id = ?", (service_id,))


def get_notes() -> str:
    with get_connection() as conn:
        row = conn.execute("SELECT content FROM notes WHERE id = 1").fetchone()
        return row["content"] if row else ""


def update_notes(content: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET content = ?, updated_at = ? WHERE id = 1",
            (content.strip(), utc_now()),
        )
