# Architecture

## Portfolio architecture

```mermaid
flowchart LR
  C[Client / Streamlit] --> API[FastAPI / Cloud Run]
  API --> O[ADK Orchestrator]
  O --> G[General Fact Agent]
  O --> GEO[Geo Validator]
  GEO --> DET[Deterministic Geo Tools]
  API --> RISK[Risk Scoring]
  API --> EVT[Audit Event]
  EVT --> PUB[Pub/Sub]
  PUB --> RAW[GCS Raw Zone]
  PUB --> BQ[BigQuery Analytics]
  BQ --> KPI[Data Quality + KPI Layer]
  KPI --> DASH[Looker / BI]
  O --> VAI[Gemini / Vertex AI]
  API --> LOG[Cloud Logging]
```

The repository deliberately supports a local SQLite warehouse so tests and demos do not require GCP. The Terraform design maps the same event model to GCS + BigQuery + Pub/Sub for a cloud deployment.

## Engineering decisions

- Deterministic numeric tools are used before LLM judgment when possible.
- Every audit emits an analytics event with latency, confidence, risk and evidence features.
- A data-quality gate checks events before persistence.
- The serving layer exposes structured Pydantic contracts suitable for downstream applications.
- Evaluation is executable in CI, making prompt/model changes measurable rather than subjective.
