-- Rows returned by this query violate analytics quality expectations.
SELECT *
FROM `PROJECT_ID.llm_auditor_analytics.audit_events`
WHERE audit_id IS NULL
   OR created_at IS NULL
   OR verdict NOT IN ('Accurate', 'Inaccurate', 'Needs Review')
   OR confidence NOT BETWEEN 0 AND 1
   OR risk_score NOT BETWEEN 0 AND 1
   OR latency_ms < 0
   OR evidence_count < 1;
