variable "project_id" {
  description = "El ID del proyecto en Google Cloud"
  type        = string
  default     = "mi-proyecto-ecommerce-123" 
}

variable "region" {
  description = "La región donde se crearán los recursos"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "El ambiente a desplegar (dev, test o prod)"
  type        = string
  default     = "dev"
}
