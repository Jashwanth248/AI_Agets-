-- BigQuery-ready KPI query for a Looker Studio dashboard.
SELECT
  DATE(created_at) AS audit_date,
  pipeline,
  verdict,
  COUNT(*) AS audit_count,
  AVG(confidence) AS avg_confidence,
  AVG(risk_score) AS avg_risk_score,
  APPROX_QUANTILES(latency_ms, 100)[OFFSET(50)] AS p50_latency_ms,
  APPROX_QUANTILES(latency_ms, 100)[OFFSET(95)] AS p95_latency_ms,
  AVG(evidence_count) AS avg_evidence_count
FROM `PROJECT_ID.llm_auditor_analytics.audit_events`
GROUP BY 1, 2, 3
ORDER BY audit_date DESC, audit_count DESC;
