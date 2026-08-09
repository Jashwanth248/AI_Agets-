from data_pipeline.warehouse import AuditWarehouse


def test_warehouse_roundtrip(tmp_path):
    db = AuditWarehouse(str(tmp_path / "audit.db"))
    db.write_event(
        {
            "audit_id": "abc",
            "created_at": "2026-08-08T00:00:00+00:00",
            "pipeline": "geo_distance",
            "verdict": "Accurate",
            "confidence": 0.9,
            "risk_score": 0.1,
            "latency_ms": 10,
            "deviation_pct": 2.0,
            "input_length": 50,
            "evidence_count": 1,
        }
    )
    assert db.summary()["audits"] == 1
    assert db.recent(1)[0]["audit_id"] == "abc"
