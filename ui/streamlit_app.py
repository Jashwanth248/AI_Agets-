from __future__ import annotations

import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="LLM Auditor Platform", layout="wide")
st.title("LLM Auditor Platform")
st.caption("Deterministic verification + audit analytics + ML risk scoring")

with st.sidebar:
    st.header("Analytics")
    if st.button("Refresh KPIs"):
        try:
            data = requests.get(f"{API_BASE_URL}/v1/analytics/summary", timeout=5).json()
            st.metric("Audits", data["audits"])
            st.metric("Avg confidence", f"{data['avg_confidence']:.2%}")
            st.metric("Avg risk", f"{data['avg_risk_score']:.2%}")
            st.metric("Avg latency", f"{data['avg_latency_ms']:.1f} ms")
        except requests.RequestException as exc:
            st.error(f"API unavailable: {exc}")

st.subheader("Verify a distance claim")
question = st.text_input("Question", "How far is Paris from London?")
claim = st.text_input("Claim", "Paris is about 900 km from London.")

c1, c2 = st.columns(2)
with c1:
    lat1 = st.number_input("Latitude A", value=48.8566, format="%.6f")
    lon1 = st.number_input("Longitude A", value=2.3522, format="%.6f")
with c2:
    lat2 = st.number_input("Latitude B", value=51.5074, format="%.6f")
    lon2 = st.number_input("Longitude B", value=-0.1278, format="%.6f")

claimed = st.number_input("Claimed distance (km)", min_value=0.0, value=900.0)
tolerance = st.slider("Tolerance (%)", min_value=0, max_value=50, value=10)

if st.button("Run audit", type="primary"):
    payload = {
        "question": question,
        "claim": claim,
        "lat1": lat1,
        "lon1": lon1,
        "lat2": lat2,
        "lon2": lon2,
        "claimed_distance_km": claimed,
        "tolerance_pct": tolerance,
    }
    try:
        response = requests.post(f"{API_BASE_URL}/v1/verify/distance", json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        a, b, c = st.columns(3)
        a.metric("Verdict", result["verdict"])
        b.metric("Confidence", f"{result['confidence']:.1%}")
        c.metric("Risk score", f"{result['risk_score']:.1%}")
        st.write(result["explanation"])
        st.json(result)
    except requests.RequestException as exc:
        st.error(f"Audit request failed: {exc}")
