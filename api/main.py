from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Query

from analytics.quality import validate_audit_event
from core.schemas import Evidence, GeoDistanceRequest, Verdict
from data_pipeline.warehouse import AuditWarehouse
from geo_toolkit import compare_claimed_distance
from ml.risk_model import RiskFeatures, confidence_from_deviation, heuristic_risk_score

warehouse: AuditWarehouse | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global warehouse
    warehouse = AuditWarehouse()
    yield


app = FastAPI(
    title="LLM Auditor Platform",
    version="2.0.0",
    description="Production-shaped multi-agent fact checking, deterministic validation, analytics, and ML risk scoring.",
    lifespan=lifespan,
)


def get_warehouse() -> AuditWarehouse:
    global warehouse
    if warehouse is None:
        warehouse = AuditWarehouse()
    return warehouse


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "llm-auditor-platform", "version": "2.0.0"}


@app.post("/v1/verify/distance", response_model=Verdict)
def verify_distance(request: GeoDistanceRequest) -> Verdict:
    started = time.perf_counter()
    calculation = compare_claimed_distance(
        request.lat1,
        request.lon1,
        request.lat2,
        request.lon2,
        request.claimed_distance_km,
        request.tolerance_pct,
    )
    deviation = float(calculation["deviation_pct"])
    features = RiskFeatures(
        deviation_pct=deviation,
        evidence_count=1,
        input_length=len(request.claim),
        deterministic_check=True,
    )
    risk_score = heuristic_risk_score(features)
    confidence = confidence_from_deviation(deviation, 1)
    verdict = Verdict(
        verdict=calculation["verdict"],
        confidence=confidence,
        risk_score=risk_score,
        corrected_value=float(calculation["actual_distance_km"]),
        explanation=(
            f"Haversine distance is {calculation['actual_distance_km']} km; the claim differs by "
            f"{deviation}% with a {request.tolerance_pct}% tolerance."
        ),
        evidence=[
            Evidence(
                source_type="deterministic",
                source="geo_toolkit.haversine_distance_km",
                detail=f"Computed great-circle distance: {calculation['actual_distance_km']} km",
            )
        ],
    )
    latency_ms = (time.perf_counter() - started) * 1000
    event = {
        "audit_id": verdict.audit_id,
        "created_at": verdict.created_at.isoformat(),
        "pipeline": "geo_distance",
        "verdict": verdict.verdict,
        "confidence": verdict.confidence,
        "risk_score": verdict.risk_score,
        "latency_ms": round(latency_ms, 3),
        "deviation_pct": deviation,
        "input_length": len(request.claim),
        "evidence_count": len(verdict.evidence),
    }
    quality = validate_audit_event(event)
    if not quality["passed"]:
        raise RuntimeError(f"Audit event failed data quality checks: {quality}")
    get_warehouse().write_event(event)
    return verdict


@app.get("/v1/analytics/summary")
def analytics_summary() -> dict[str, Any]:
    return get_warehouse().summary()


@app.get("/v1/events")
def recent_events(limit: int = Query(default=100, ge=1, le=1000)) -> list[dict[str, Any]]:
    return get_warehouse().recent(limit=limit)
