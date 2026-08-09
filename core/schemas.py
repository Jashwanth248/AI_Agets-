from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class GeoDistanceRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    claim: str = Field(min_length=3, max_length=4000)
    lat1: float = Field(ge=-90, le=90)
    lon1: float = Field(ge=-180, le=180)
    lat2: float = Field(ge=-90, le=90)
    lon2: float = Field(ge=-180, le=180)
    claimed_distance_km: float = Field(ge=0)
    tolerance_pct: float = Field(default=10.0, ge=0, le=100)


class Evidence(BaseModel):
    source_type: Literal["deterministic", "web", "dataset", "model"]
    source: str
    detail: str


class Verdict(BaseModel):
    audit_id: str = Field(default_factory=lambda: str(uuid4()))
    verdict: Literal["Accurate", "Inaccurate", "Needs Review"]
    confidence: float = Field(ge=0, le=1)
    risk_score: float = Field(ge=0, le=1)
    corrected_value: float | None = None
    explanation: str
    evidence: list[Evidence]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
