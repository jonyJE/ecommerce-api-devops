output "service_id" {
  description = "Identificador del servicio creado en Render"
  value       = render_web_service.api.id
}

output "service_url" {
  description = "URL pública de la API"
  value       = render_web_service.api.url
}

output "environment" {
  description = "Ambiente desplegado"
  value       = var.environment
}
