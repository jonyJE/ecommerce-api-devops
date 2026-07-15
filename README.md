# API de Catálogo de Productos — DevOps

[![CI - Tests, Docker and Security](https://github.com/jonyJE/ecommerce-api-devops/actions/workflows/pipeline.yml/badge.svg)](https://github.com/jonyJE/ecommerce-api-devops/actions/workflows/pipeline.yml)

API REST para administrar el catálogo de productos de un e-commerce, implementada con FastAPI y MongoDB Atlas. El proyecto incorpora prácticas DevOps como contenedores Docker, CI/CD, infraestructura como código, monitoreo y análisis de vulnerabilidades.

## Problema de negocio

Una tienda en línea puede perder ventas cuando su catálogo de productos deja de estar disponible durante picos de tráfico o cuando cada actualización requiere detener el sistema.

La solución busca:

- Mantener disponible el catálogo de productos.
- Automatizar pruebas, construcción y despliegue.
- Realizar despliegues sin intervención manual.
- Detectar vulnerabilidades antes de publicar cambios.
- Supervisar el estado y rendimiento de la API.
- Administrar la infraestructura mediante código.

## Solución implementada

El proyecto utiliza los siguientes componentes:

| Componente | Tecnología | Propósito |
|---|---|---|
| API REST | FastAPI | Gestión del catálogo de productos |
| Base de datos | MongoDB Atlas | Persistencia administrada en la nube |
| Contenedores | Docker y Docker Compose | Ejecución reproducible |
| CI/CD | GitHub Actions | Pruebas, validaciones, seguridad y despliegue |
| Registro de imágenes | GitHub Container Registry | Publicación de imágenes Docker |
| Seguridad | Trivy | Escaneo de vulnerabilidades |
| Infraestructura como código | Terraform | Aprovisionamiento del servicio en Render |
| Despliegue | Render | Ejecución pública de la API |
| Métricas | Prometheus | Recolección de métricas |
| Visualización | Grafana | Dashboard de observabilidad |

## Arquitectura

```mermaid
flowchart TD
    U[Cliente] --> R[API en Render]
    R --> M[(MongoDB Atlas)]

    G[GitHub] --> A[GitHub Actions]
    A --> T[Tests y Terraform]
    T --> S[Docker y Trivy]
    S --> D[Deploy Hook]
    D --> R

    P[Prometheus] --> L[API local]
    F[Grafana] --> P
```

En desarrollo local, Docker Compose ejecuta la API, Prometheus y Grafana dentro de una red privada.

En el ambiente desplegado, Render ejecuta la imagen Docker y se conecta con MongoDB Atlas mediante variables de entorno protegidas.

## Funcionalidades de la API

La API permite:

- Crear productos.
- Listar hasta 100 productos.
- Consultar un producto por identificador.
- Actualizar productos.
- Eliminar productos.
- Validar los datos de entrada.
- Comprobar el estado de la aplicación.
- Comprobar la conexión con MongoDB.
- Exportar métricas para Prometheus.

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Mensaje de estado general |
| `GET` | `/health` | Comprueba que el proceso de la API funciona |
| `GET` | `/ready` | Comprueba la conexión con MongoDB Atlas |
| `GET` | `/productos` | Lista los productos |
| `GET` | `/productos/{id}` | Obtiene un producto |
| `POST` | `/productos` | Crea un producto |
| `PUT` | `/productos/{id}` | Actualiza un producto |
| `DELETE` | `/productos/{id}` | Elimina un producto |
| `GET` | `/metrics` | Expone métricas para Prometheus |
| `GET` | `/docs` | Documentación interactiva Swagger |

## Modelo de producto

```json
{
  "nombre": "Laptop Lenovo",
  "descripcion": "Laptop para trabajo y estudios",
  "precio": 2499.90,
  "stock": 10
}
```

Reglas principales:

- `nombre`: obligatorio, entre 2 y 100 caracteres.
- `descripcion`: opcional, máximo 500 caracteres.
- `precio`: obligatorio y mayor que cero.
- `stock`: entero igual o mayor que cero.

## Requisitos

Para ejecutar el proyecto localmente se necesita:

- Git.
- Docker con Docker Compose.
- Una cuenta gratuita de MongoDB Atlas.
- Acceso a GitHub Codespaces o un entorno Linux compatible.

Terraform solo es necesario para validar o modificar la infraestructura de Render.

## Variables de entorno

Crear un archivo `.env` a partir del ejemplo:

```bash
cp .env.example .env
```

Configurar las siguientes variables:

```dotenv
MONGODB_URI=mongodb+srv://USUARIO:CONTRASENA@CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=ecommerce
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=CAMBIAR_POR_UNA_CONTRASENA_SEGURA
```

El archivo `.env` está excluido del repositorio mediante `.gitignore` y nunca debe subirse a GitHub.

Cuando se utiliza GitHub Codespaces, la IP pública de salida del Codespace debe agregarse manualmente a la lista de acceso de MongoDB Atlas.

## Ejecución con Docker Compose

Construir e iniciar todos los servicios:

```bash
docker compose up -d --build
```

Verificar los contenedores:

```bash
docker compose ps
```

Servicios disponibles:

| Servicio | Dirección |
|---|---|
| API | `http://localhost:8080` |
| Swagger | `http://localhost:8080/docs` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |

Comprobar disponibilidad:

```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/ready
```

Detener los servicios:

```bash
docker compose down
```

## Ejemplos de uso

Crear un producto:

```bash
curl -X POST http://localhost:8080/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Lenovo",
    "descripcion": "Laptop para trabajo y estudios",
    "precio": 2499.90,
    "stock": 10
  }'
```

Listar productos:

```bash
curl http://localhost:8080/productos
```

Consultar un producto:

```bash
curl http://localhost:8080/productos/IDENTIFICADOR
```

Actualizar un producto:

```bash
curl -X PUT http://localhost:8080/productos/IDENTIFICADOR \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 2399.90,
    "stock": 15
  }'
```

Eliminar un producto:

```bash
curl -X DELETE http://localhost:8080/productos/IDENTIFICADOR
```

## Pruebas automáticas

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar las pruebas:

```bash
python -m pytest -v
```

Las pruebas utilizan `mongomock`, por lo que no modifican los datos reales de MongoDB Atlas.

Actualmente se validan:

- Endpoint principal.
- Endpoint de salud.
- Flujo CRUD completo.
- Rechazo de precios negativos.
- Rechazo de identificadores inválidos.

## Pipeline CI/CD

El workflow se encuentra en:

```text
.github/workflows/pipeline.yml
```

Se ejecuta con cambios en las ramas `main` y `develop`, en pull requests hacia `main` y manualmente mediante `workflow_dispatch`.

El pipeline contiene cuatro trabajos:

1. **Pruebas automáticas**
   - Descarga el código.
   - Configura Python.
   - Instala dependencias.
   - Ejecuta Pytest.

2. **Validación Terraform**
   - Inicializa Terraform sin backend remoto.
   - Comprueba el formato.
   - Valida la configuración.

3. **Docker y seguridad**
   - Construye la imagen Docker.
   - Reporta vulnerabilidades altas y críticas.
   - Bloquea la publicación si existen vulnerabilidades críticas corregibles.
   - Publica la imagen en GitHub Container Registry.

4. **Despliegue en Render**
   - Se ejecuta únicamente desde `main`.
   - Espera que las pruebas, Terraform y seguridad finalicen correctamente.
   - Solicita el despliegue mediante un Deploy Hook protegido como secreto.

## Infraestructura como código

Terraform administra el servicio web de Render.

Archivos principales:

```text
terraform/
├── environments/
│   ├── dev.tfvars
│   ├── test.tfvars
│   └── prod.tfvars
├── main.tf
├── outputs.tf
└── variables.tf
```

Perfiles definidos:

| Ambiente | Plan | Instancias | Base de datos |
|---|---:|---:|---|
| Desarrollo | Free | 1 | `ecommerce` |
| Pruebas | Free | 1 | `ecommerce_test` |
| Producción | Starter | 2 | `ecommerce_prod` |

El perfil de producción representa el diseño de alta disponibilidad y no debe aplicarse sin revisar previamente los costos.

Validar Terraform:

```bash
cd terraform
terraform init
terraform fmt -check -recursive
terraform validate
```

Generar un plan para desarrollo:

```bash
terraform plan -var-file=environments/dev.tfvars
```

Generar un plan para pruebas:

```bash
terraform plan -var-file=environments/test.tfvars
```

Generar un plan para producción:

```bash
terraform plan -var-file=environments/prod.tfvars
```

Las credenciales de Render y la URI de MongoDB se proporcionan mediante variables de entorno y no se almacenan en los archivos `.tfvars`.

## Monitoreo

Prometheus consulta el endpoint `/metrics` de la API cada cinco segundos.

Grafana se configura automáticamente mediante archivos versionados en:

```text
grafana/provisioning/
```

El dashboard **E-commerce API - Observabilidad** incluye:

- Estado de disponibilidad de la API.
- Tasa de solicitudes por segundo.
- Errores HTTP 5xx.
- Latencia p95.
- Consumo de CPU.
- Consumo de memoria.

El dashboard está definido como código en:

```text
grafana/provisioning/dashboards/json/ecommerce-api.json
```

## Seguridad

Controles implementados:

- Contenedor ejecutado con un usuario sin privilegios.
- Variables sensibles fuera del repositorio.
- Archivo `.dockerignore` para reducir el contexto de construcción.
- Usuario de MongoDB limitado a `readWrite` sobre la base necesaria.
- Restricción de acceso de red en MongoDB Atlas.
- Escaneo automático de imágenes con Trivy.
- Bloqueo del pipeline ante vulnerabilidades críticas corregibles.
- Credenciales administradas mediante GitHub Actions Secrets.
- Archivos de estado de Terraform excluidos del repositorio.
- Dependencias con versiones fijadas.

## Despliegue

La API de desarrollo se encuentra desplegada en Render.

La URL puede consultarse mediante Terraform:

```bash
cd terraform
terraform output -raw service_url
```

Validar el servicio desplegado:

```bash
SERVICE_URL=$(terraform output -raw service_url)

curl -i "$SERVICE_URL/health"
curl -i "$SERVICE_URL/ready"
curl "$SERVICE_URL/openapi.json"
```

Render ejecuta un despliegue administrado después de que el pipeline finaliza correctamente. Esto permite actualizar la aplicación sin detener manualmente el servicio anterior.

## Estructura del repositorio

```text
.
├── .github/workflows/pipeline.yml
├── grafana/provisioning
│   ├── dashboards
│   │   ├── json/ecommerce-api.json
│   │   └── provider.yml
│   └── datasources/prometheus.yml
├── terraform
│   ├── environments
│   │   ├── dev.tfvars
│   │   ├── test.tfvars
│   │   └── prod.tfvars
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── prometheus.yml
├── requirements.txt
└── test_main.py
```

## Limitaciones conocidas

- El plan gratuito de Render puede suspender el servicio después de un periodo de inactividad y provocar una demora inicial.
- El ambiente local depende de la IP pública asignada al Codespace.
- Los perfiles `test` y `prod` están definidos mediante Terraform, pero no se aprovisionan permanentemente para evitar costos innecesarios.
- La alta disponibilidad real requiere aplicar el perfil de producción con al menos dos instancias.
