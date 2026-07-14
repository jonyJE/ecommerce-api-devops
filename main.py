from fastapi import FastAPI
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# ¡Esta sola línea activa el monitoreo automático de toda la API!
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"mensaje": "API de Catálogo de Productos - Funcionando"}

@app.get("/productos")
def get_productos():
    # Conexión futura a PostgreSQL
    return {"productos": ["Laptop", "Mouse", "Teclado"]}
