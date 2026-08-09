from analytics.quality import validate_audit_event


def test_valid_event_passes_quality_gate():
    event = {
        "audit_id": "1",
        "verdict": "Accurate",
        "confidence": 0.9,
        "risk_score": 0.1,
        "latency_ms": 12.5,
        "evidence_count": 2,
    }
    result = validate_audit_event(event)
    assert result["passed"] is True
    assert result["score"] == 1.0
