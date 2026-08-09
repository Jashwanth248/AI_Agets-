output "cloud_run_uri" { value = google_cloud_run_v2_service.api.uri }
output "raw_bucket" { value = google_storage_bucket.raw_audit_events.name }
output "analytics_dataset" { value = google_bigquery_dataset.analytics.dataset_id }
output "audit_topic" { value = google_pubsub_topic.audit_events.name }
