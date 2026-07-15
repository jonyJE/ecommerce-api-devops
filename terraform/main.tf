terraform {
  required_version = ">= 1.6.0"

  required_providers {
    render = {
      source  = "render-oss/render"
      version = "1.8.0"
    }
  }
}

# Las credenciales se leen automáticamente desde:
# RENDER_API_KEY y RENDER_OWNER_ID
provider "render" {}

resource "render_web_service" "api" {
  name              = "ecommerce-api-${var.environment}"
  plan              = var.service_plan
  region            = var.region
  health_check_path = "/health"
  num_instances = var.instance_count

  runtime_source = {
    docker = {
      repo_url            = var.repository_url
      branch              = var.branch
      dockerfile_path     = "./Dockerfile"
      context             = "."
      auto_deploy_trigger = "checksPass"
    }
  }

  env_vars = {
    ENVIRONMENT = {
      value = var.environment
    }

    MONGODB_URI = {
      value = var.mongodb_uri
    }

    MONGODB_DB_NAME = {
      value = var.mongodb_db_name
    }
  }
}
