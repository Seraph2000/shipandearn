import sqlite3
import csv
import json
import os
from datetime import date
from typing import Optional
import config


def get_conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                platform            TEXT NOT NULL,
                task_id             TEXT NOT NULL,
                title               TEXT,
                pay                 REAL,
                estimated_minutes   REAL,
                category            TEXT,
                link                TEXT,
                timestamp           TEXT,
                metadata            TEXT,
                score               REAL DEFAULT 0,
                status              TEXT DEFAULT 'available',
                UNIQUE(platform, task_id)
            );

            CREATE TABLE IF NOT EXISTS completions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                platform        TEXT,
                task_id         TEXT,
                title           TEXT,
                pay             REAL,
                actual_minutes  REAL,
                completed_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS ai_cache (
                prompt_hash TEXT PRIMARY KEY,
                response    TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );
        """)


def upsert_task(task: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO tasks
                (platform, task_id, title, pay, estimated_minutes, category, link, timestamp, metadata, score)
            VALUES
                (:platform, :task_id, :title, :pay, :estimated_minutes, :category, :link, :timestamp, :metadata, :score)
            ON CONFLICT(platform, task_id) DO UPDATE SET
                title             = excluded.title,
                pay               = excluded.pay,
                estimated_minutes = excluded.estimated_minutes,
                score             = excluded.score,
                status            = CASE WHEN tasks.status = 'completed' THEN 'completed' ELSE 'available' END
        """, {**task, "metadata": json.dumps(task.get("metadata", {}))})


def get_available_tasks():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = 'available' ORDER BY score DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def mark_completed(platform: str, task_id: str, actual_minutes: float, pay: float, title: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET status = 'completed' WHERE platform = ? AND task_id = ?",
            (platform, task_id),
        )
        conn.execute(
            "INSERT INTO completions (platform, task_id, title, pay, actual_minutes) VALUES (?,?,?,?,?)",
            (platform, task_id, title, pay, actual_minutes),
        )
    _append_to_csv(platform, task_id, title, pay, actual_minutes)


def get_earnings_today() -> dict:
    with get_conn() as conn:
        row = conn.execute("""
            SELECT COALESCE(SUM(pay), 0)            AS total_pay,
                   COALESCE(SUM(actual_minutes), 0) AS total_minutes,
                   COUNT(*)                          AS tasks_completed
            FROM completions
            WHERE date(completed_at) = date('now')
        """).fetchone()
        return dict(row)


def get_earnings_this_month() -> dict:
    with get_conn() as conn:
        row = conn.execute("""
            SELECT COALESCE(SUM(pay), 0) AS total_pay,
                   COUNT(*)              AS tasks_completed
            FROM completions
            WHERE strftime('%Y-%m', completed_at) = strftime('%Y-%m', 'now')
        """).fetchone()
        return dict(row)


def get_recent_completions(limit: int = 20):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM completions ORDER BY completed_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_ai_cached(prompt_hash: str) -> Optional[str]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT response FROM ai_cache WHERE prompt_hash = ?", (prompt_hash,)
        ).fetchone()
        return row["response"] if row else None


def set_ai_cache(prompt_hash: str, response: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO ai_cache (prompt_hash, response) VALUES (?,?)",
            (prompt_hash, response),
        )


def _append_to_csv(platform, task_id, title, pay, actual_minutes):
    write_header = not os.path.exists(config.EARNINGS_CSV)
    with open(config.EARNINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["date", "platform", "task_id", "title", "pay_gbp", "minutes", "gbp_per_hour"])
        gbp_per_hour = round(pay / actual_minutes * 60, 2) if actual_minutes > 0 else 0
        writer.writerow([date.today().isoformat(), platform, task_id, title, pay, actual_minutes, gbp_per_hour])
