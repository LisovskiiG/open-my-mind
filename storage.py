"""Persist one outcome per exercise and one reminder per account."""

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import os
import secrets
import sqlite3
import time
from typing import Literal
from uuid import uuid4

Outcome = Literal[
    "independent", "guided", "direct", "revealed_after_attempt",
    "quiz_correct", "quiz_incorrect",
]
Period = Literal["week", "month", "all_time"]
OUTCOMES = tuple(Outcome.__args__)
DAY = 86_400


@contextmanager
def database():
    db = sqlite3.connect(os.environ.get("OPENMYMIND_DB", "openmymind.sqlite3"), timeout=10)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize():
    with database() as db:
        db.executescript("""
            PRAGMA journal_mode = WAL;
            CREATE TABLE IF NOT EXISTS analytics (
                account TEXT PRIMARY KEY, enabled INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS exercises (
                id TEXT PRIMARY KEY, account TEXT NOT NULL, outcome TEXT,
                completed_at INTEGER
            );
            CREATE INDEX IF NOT EXISTS exercises_by_account
                ON exercises(account, completed_at);
            CREATE TABLE IF NOT EXISTS reminders (
                account TEXT PRIMARY KEY, email TEXT NOT NULL, days INTEGER NOT NULL,
                due_at INTEGER NOT NULL, unsubscribe_token TEXT UNIQUE NOT NULL,
                claim TEXT, claim_until INTEGER, failures INTEGER NOT NULL DEFAULT 0
            );
        """)


def analytics_enabled(db, account):
    row = db.execute("SELECT enabled FROM analytics WHERE account = ?", (account,)).fetchone()
    return bool(row and row["enabled"])


def set_analytics(account, enabled):
    with database() as db:
        db.execute(
            "INSERT INTO analytics VALUES (?, ?) ON CONFLICT(account) "
            "DO UPDATE SET enabled = excluded.enabled", (account, enabled),
        )
        if not enabled:
            db.execute("DELETE FROM exercises WHERE account = ? AND outcome IS NULL", (account,))


def start_exercise(account):
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        if not analytics_enabled(db, account):
            return None
        exercise = uuid4().hex
        db.execute("INSERT INTO exercises (id, account) VALUES (?, ?)", (exercise, account))
        return exercise


def record(account, exercise, outcome):
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        if not analytics_enabled(db, account):
            return "tracking_disabled"
        row = db.execute(
            "SELECT outcome FROM exercises WHERE id = ? AND account = ?", (exercise, account),
        ).fetchone()
        if row is None:
            return "exercise_not_found"
        if row["outcome"] is not None:
            return "already_recorded" if row["outcome"] == outcome else "outcome_conflict"
        db.execute(
            "UPDATE exercises SET outcome = ?, completed_at = ? WHERE id = ?",
            (outcome, int(time.time()), exercise),
        )
        return "recorded"


def score(counts):
    base = sum(counts[key] for key in ("independent", "guided", "direct", "revealed_after_attempt"))
    return round(100 * counts["independent"] / base, 1) if base else None


def progress(account, period, now=None):
    now = now or datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    days = {"week": 7, "month": 30}.get(period)
    start = int((today - timedelta(days=days - 1)).timestamp()) if days else 0
    pattern = "%Y-%m-%d" if days else "%Y-%m"
    with database() as db:
        rows = db.execute(
            "SELECT strftime(?, completed_at, 'unixepoch') AS bucket, outcome, count(*) AS n "
            "FROM exercises WHERE account = ? AND completed_at BETWEEN ? AND ? "
            "GROUP BY bucket, outcome ORDER BY bucket", (pattern, account, start, int(now.timestamp())),
        ).fetchall()
    totals = dict.fromkeys(OUTCOMES, 0)
    buckets = {}
    for row in rows:
        counts = buckets.setdefault(row["bucket"], dict.fromkeys(OUTCOMES, 0))
        counts[row["outcome"]] += row["n"]
        totals[row["outcome"]] += row["n"]
    return {
        "period": period, "time_zone": "UTC", "counts": totals,
        "independence_percent": score(totals),
        "series": [
            {"bucket": bucket, "independence_percent": score(counts)}
            for bucket, counts in buckets.items()
        ],
    }


def reminder(account):
    with database() as db:
        row = db.execute(
            "SELECT days, due_at, failures FROM reminders WHERE account = ?", (account,),
        ).fetchone()
    if row is None:
        return {"enabled": False}
    return {
        "enabled": True,
        "cadence": "daily" if row["days"] == 1 else "every_three_days",
        "next_due_utc": datetime.fromtimestamp(row["due_at"], timezone.utc).isoformat(),
        "retry_pending": row["failures"] > 0,
    }


def schedule(account, email, days):
    with database() as db:
        db.execute(
            "INSERT INTO reminders (account, email, days, due_at, unsubscribe_token) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(account) DO UPDATE SET email = excluded.email, days = excluded.days, "
            "due_at = excluded.due_at, claim = NULL, claim_until = NULL, failures = 0 "
            "WHERE reminders.days <> excluded.days OR reminders.email <> excluded.email",
            (account, email, days, int(time.time()) + days * DAY, secrets.token_urlsafe(32)),
        )


def disable(account):
    with database() as db:
        db.execute("DELETE FROM reminders WHERE account = ?", (account,))


def unsubscribe(token):
    with database() as db:
        db.execute("DELETE FROM reminders WHERE unsubscribe_token = ?", (token,))


def claim_due(now, after=None):
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute(
            "SELECT * FROM reminders WHERE due_at <= ? AND coalesce(claim_until, 0) <= ? "
            "AND (? IS NULL OR account > ?) ORDER BY account LIMIT 1", (now, now, after, after),
        ).fetchone()
        if row is None:
            return None
        claim = secrets.token_hex(16)
        db.execute("UPDATE reminders SET claim = ?, claim_until = ? WHERE account = ?",
                   (claim, now + 600, row["account"]))
        return {**row, "claim": claim}


def claim_is_current(account, claim):
    with database() as db:
        return db.execute("SELECT 1 FROM reminders WHERE account = ? AND claim = ?",
                          (account, claim)).fetchone() is not None


def finish_delivery(item, delivered, now):
    failures = 0 if delivered else item["failures"] + 1
    delay = item["days"] * DAY if delivered else min(DAY, 900 * (2 ** min(failures - 1, 7)))
    with database() as db:
        db.execute(
            "UPDATE reminders SET due_at = ?, failures = ?, claim = NULL, claim_until = NULL "
            "WHERE account = ? AND claim = ?",
            (now + delay, failures, item["account"], item["claim"]),
        )
