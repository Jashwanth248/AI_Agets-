terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "pubsub.googleapis.com",
    "aiplatform.googleapis.com",
    "logging.googleapis.com",
  ])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_storage_bucket" "raw_audit_events" {
  name                        = "${var.project_id}-llm-auditor-raw"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
  lifecycle_rule {
    condition { age = 30 }
    action { type = "SetStorageClass" storage_class = "NEARLINE" }
  }
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "llm_auditor_analytics"
  location   = var.region
}

resource "google_pubsub_topic" "audit_events" {
  name = "llm-auditor-events"
}

resource "google_cloud_run_v2_service" "api" {
  name     = var.service_name
  location = var.region
  template {
    containers {
      image = var.image
      env { name = "ENABLE_CLOUD_LOGGING" value = "true" }
      env { name = "GOOGLE_CLOUD_PROJECT" value = var.project_id }
      resources { limits = { cpu = "1", memory = "1Gi" } }
    }
    scaling { min_instance_count = 0 max_instance_count = 5 }
  }
  depends_on = [google_project_service.apis]
}
