"""Deterministic geospatial tools for the geo_validator agent."""

from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0088


def validate_coordinates(latitude: float, longitude: float) -> dict:
    errors = []
    if not -90 <= latitude <= 90:
        errors.append(f"latitude {latitude} is outside the valid range [-90, 90]")
    if not -180 <= longitude <= 180:
        errors.append(f"longitude {longitude} is outside the valid range [-180, 180]")
    if errors:
        return {"is_valid": False, "reason": "; ".join(errors)}
    return {"is_valid": True, "reason": f"({latitude}, {longitude}) is a valid coordinate pair."}


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> dict:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return {"distance_km": round(EARTH_RADIUS_KM * c, 1)}


def compare_claimed_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    claimed_distance_km: float,
    tolerance_pct: float = 10.0,
) -> dict:
    actual = haversine_distance_km(lat1, lon1, lat2, lon2)["distance_km"]
    if actual == 0:
        deviation_pct = 0.0 if claimed_distance_km == 0 else float("inf")
    else:
        deviation_pct = abs(claimed_distance_km - actual) / actual * 100
    verdict = "Accurate" if deviation_pct <= tolerance_pct else "Inaccurate"
    return {
        "actual_distance_km": actual,
        "claimed_distance_km": claimed_distance_km,
        "deviation_pct": round(deviation_pct, 1),
        "verdict": verdict,
    }
