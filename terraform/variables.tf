variable "environment" {
  description = "Ambiente que se desplegará: dev, test o prod"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "El ambiente debe ser dev, test o prod."
  }
}

variable "region" {
  description = "Región de Render donde se ejecutará la API"
  type        = string
  default     = "virginia"

  validation {
    condition = contains(
      ["frankfurt", "ohio", "oregon", "singapore", "virginia"],
      var.region
    )
    error_message = "La región seleccionada no es compatible con Render."
  }
}

variable "service_plan" {
  description = "Plan utilizado por el servicio de Render"
  type        = string
  default     = "free"
}

variable "repository_url" {
  description = "Repositorio GitHub que contiene la API"
  type        = string
  default     = "https://github.com/jonyJE/ecommerce-api-devops"
}

variable "branch" {
  description = "Rama que Render debe desplegar"
  type        = string
  default     = "main"
}

variable "mongodb_uri" {
  description = "Cadena privada de conexión a MongoDB Atlas"
  type        = string
  sensitive   = true
}

variable "mongodb_db_name" {
  description = "Nombre de la base de datos MongoDB"
  type        = string
  default     = "ecommerce"
}
