# 1. Usamos una versión ligera de Python como base
FROM python:3.9-slim

# 2. Creamos una carpeta llamada /app dentro del contenedor
WORKDIR /app

# 3. Copiamos nuestro archivo de requisitos a la carpeta /app
COPY requirements.txt .

# 4. Instalamos las herramientas que listamos en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de nuestro código (el main.py)
COPY . .

# 6. Le decimos al contenedor cómo arrancar nuestra API
# Usamos el puerto 8080 porque es el estándar que pide Google Cloud Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
