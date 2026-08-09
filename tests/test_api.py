import os

os.environ["AUDIT_DB_PATH"] = "/tmp/llm_auditor_test_api.db"

from fastapi.testclient import TestClient

from api.main import app


def test_healthz():
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_distance_verification():
    with TestClient(app) as client:
        response = client.post(
            "/v1/verify/distance",
            json={
                "question": "How far are Paris and London?",
                "claim": "Paris is 900 km from London.",
                "lat1": 48.8566,
                "lon1": 2.3522,
                "lat2": 51.5074,
                "lon2": -0.1278,
                "claimed_distance_km": 900,
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["verdict"] == "Inaccurate"
        assert 340 <= body["corrected_value"] <= 350
