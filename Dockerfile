# Imagen ligera y compatible con el entorno del proyecto
FROM python:3.12-slim

# Configuración segura y optimizada de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Crear un usuario sin privilegios administrativos
RUN groupadd --system appgroup \
    && useradd --system \
        --gid appgroup \
        --create-home \
        appuser

# Instalar dependencias antes de copiar el código
# Esto permite reutilizar la caché de Docker
COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# Copiar únicamente el código necesario
COPY --chown=appuser:appgroup main.py .

# Ejecutar la aplicación como usuario no-root
USER appuser

# Puerto utilizado por la API
EXPOSE 8080

# Verificación de salud incorporada en la imagen
HEALTHCHECK \
    --interval=15s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Iniciar FastAPI mediante Uvicorn
CMD [
    "python",
    "-m",
    "uvicorn",
    "main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8080"
]
