from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API de Catálogo de Productos - Funcionando"}

@app.get("/productos")
def get_productos():
    # Aquí conectaremos más adelante a la base de datos PostgreSQL
    return {"productos": ["Laptop", "Mouse", "Teclado"]}
