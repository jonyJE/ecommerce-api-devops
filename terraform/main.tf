terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Base de Datos PostgreSQL (Cloud SQL)
resource "google_sql_database_instance" "postgres_instance" {
  name             = "ecommerce-db-${var.environment}"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier = "db-f1-micro" # Opción económica para el proyecto
  }
}

# 2. Contenedor de la API (Cloud Run)
resource "google_cloud_run_service" "api_service" {
  name     = "ecommerce-api-${var.environment}"
  location = var.region

  template {
    spec {
      containers {
        # Aquí vivirá la imagen Docker que creamos antes
        image = "gcr.io/${var.project_id}/ecommerce-api:latest"
        
        # Conexión a la BD mediante Variables de Entorno (Requisito de la rúbrica)
        env {
          name  = "DB_CONNECTION"
          value = google_sql_database_instance.postgres_instance.connection_name
        }
      }
    }
  }
}
