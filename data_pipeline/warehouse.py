from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

DEFAULT_DB_PATH = "artifacts/auditor.db"


class AuditWarehouse:
    """Small local analytical store mirroring the schema used in BigQuery."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.getenv("AUDIT_DB_PATH", DEFAULT_DB_PATH)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    audit_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    pipeline TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    risk_score REAL NOT NULL,
                    latency_ms REAL NOT NULL,
                    deviation_pct REAL,
                    input_length INTEGER NOT NULL,
                    evidence_count INTEGER NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_events_created_at ON audit_events(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_events_verdict ON audit_events(verdict)")

    def write_event(self, event: dict[str, Any]) -> None:
        required = {
            "audit_id", "created_at", "pipeline", "verdict", "confidence",
            "risk_score", "latency_ms", "input_length", "evidence_count",
        }
        missing = required - event.keys()
        if missing:
            raise ValueError(f"Missing required audit fields: {sorted(missing)}")

        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO audit_events (
                    audit_id, created_at, pipeline, verdict, confidence, risk_score,
                    latency_ms, deviation_pct, input_length, evidence_count, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["audit_id"], str(event["created_at"]), event["pipeline"],
                    event["verdict"], float(event["confidence"]), float(event["risk_score"]),
                    float(event["latency_ms"]), event.get("deviation_pct"),
                    int(event["input_length"]), int(event["evidence_count"]),
                    json.dumps(event, default=str),
                ),
            )

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 1000))
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM audit_events ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def summary(self) -> dict[str, Any]:
        with self._connect() as conn:
            totals = conn.execute(
                """
                SELECT COUNT(*) AS audits,
                       AVG(confidence) AS avg_confidence,
                       AVG(risk_score) AS avg_risk_score,
                       AVG(latency_ms) AS avg_latency_ms,
                       AVG(evidence_count) AS avg_evidence_count
                FROM audit_events
                """
            ).fetchone()
            verdict_rows = conn.execute(
                "SELECT verdict, COUNT(*) AS n FROM audit_events GROUP BY verdict"
            ).fetchall()
        return {
            "audits": int(totals["audits"] or 0),
            "avg_confidence": round(float(totals["avg_confidence"] or 0), 4),
            "avg_risk_score": round(float(totals["avg_risk_score"] or 0), 4),
            "avg_latency_ms": round(float(totals["avg_latency_ms"] or 0), 2),
            "avg_evidence_count": round(float(totals["avg_evidence_count"] or 0), 2),
            "verdict_counts": {row["verdict"]: row["n"] for row in verdict_rows},
        }
