from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskFeatures:
    deviation_pct: float
    evidence_count: int
    input_length: int
    deterministic_check: bool = True


def heuristic_risk_score(features: RiskFeatures) -> float:
    """Calibrated, deterministic fallback risk score available without a model file.

    Production deployments can replace this with a trained sklearn/Vertex AI model;
    this fallback keeps API behavior deterministic in tests and local development.
    """
    deviation_component = min(max(features.deviation_pct, 0.0) / 100.0, 1.0)
    evidence_component = 1.0 / max(features.evidence_count, 1)
    length_component = min(features.input_length / 4000.0, 1.0)
    deterministic_discount = 0.18 if features.deterministic_check else 0.0
    raw = 0.58 * deviation_component + 0.27 * evidence_component + 0.15 * length_component
    return round(min(max(raw - deterministic_discount, 0.0), 1.0), 4)


def confidence_from_deviation(deviation_pct: float, evidence_count: int) -> float:
    """Produce an interpretable confidence score from deterministic evidence."""
    signal = 1.0 - math.exp(-abs(deviation_pct) / 15.0)
    evidence_bonus = min(evidence_count * 0.05, 0.15)
    return round(min(0.72 + 0.2 * signal + evidence_bonus, 0.99), 4)
