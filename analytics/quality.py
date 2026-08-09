from __future__ import annotations

from typing import Any

EXPECTED_VERDICTS = {"Accurate", "Inaccurate", "Needs Review"}


def validate_audit_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return explicit data-quality checks suitable for API/ETL monitoring."""
    checks = {
        "audit_id_present": bool(event.get("audit_id")),
        "valid_verdict": event.get("verdict") in EXPECTED_VERDICTS,
        "confidence_range": 0 <= float(event.get("confidence", -1)) <= 1,
        "risk_score_range": 0 <= float(event.get("risk_score", -1)) <= 1,
        "latency_nonnegative": float(event.get("latency_ms", -1)) >= 0,
        "evidence_nonempty": int(event.get("evidence_count", 0)) > 0,
    }
    passed = sum(checks.values())
    return {
        "passed": passed == len(checks),
        "score": round(passed / len(checks), 4),
        "checks": checks,
    }
