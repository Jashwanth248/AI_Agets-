# How this project maps to four job families

## Data Engineer
- Event-oriented audit schema and ingestion path.
- Local analytical warehouse plus production GCS/BigQuery/Pub/Sub architecture.
- Terraform, Cloud Build, Docker, CI, schema/data-quality checks, observability.

## Data Analyst
- Queryable audit history and KPI endpoint for volume, verdict mix, confidence, latency and evidence depth.
- Warehouse schema supports BI dashboards and trend analysis.

## Data Scientist
- Feature engineering for deviation, evidence density, text size and deterministic-validation flags.
- Risk-scoring layer for prioritizing low-confidence/high-risk audits.
- Golden-dataset evaluation and regression metrics.

## AI/ML Engineer
- Google ADK multi-agent orchestration, deterministic tools, Gemini/Vertex AI readiness.
- FastAPI model serving, structured response contracts, automated evaluation, containerization and Cloud Run deployment.
- Production-safe logging and local fallbacks.

## Strong resume bullets
- Engineered a production-shaped multi-agent LLM auditing platform on Google ADK and Vertex AI patterns, combining grounded search with deterministic geospatial tools to reduce hallucination risk.
- Designed an event-driven analytics architecture using Pub/Sub, Cloud Storage and BigQuery concepts, with schema validation, audit telemetry, KPI endpoints and reproducible local SQLite execution.
- Built FastAPI serving, Docker/Cloud Run infrastructure, Terraform IaC, Cloud Build CI/CD and automated regression evaluation for reliable ML/agent releases.
- Implemented interpretable risk scoring and confidence features to prioritize questionable LLM outputs and expose model-quality signals for downstream analytics.
