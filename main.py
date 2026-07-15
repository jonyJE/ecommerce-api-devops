import os
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import PyMongoError


# ============================================================
# CONFIGURACIÓN
# ============================================================

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ecommerce")


# La aplicación puede iniciar aunque todavía no exista la URI.
# Esto permite ejecutar las pruebas básicas sin exponer secretos.
if MONGODB_URI:
    mongo_client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )

    database = mongo_client[MONGODB_DB_NAME]
    productos_collection = database["productos"]
else:
    mongo_client = None
    database = None
    productos_collection = None


# ============================================================
# APLICACIÓN FASTAPI
# ============================================================

app = FastAPI(
    title="API de Catálogo de Productos",
    description=(
        "API REST para gestionar el catálogo de productos "
        "de una tienda e-commerce."
    ),
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)


# ============================================================
# MODELOS
# ============================================================

class ProductoCreate(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Laptop Lenovo"]
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["Laptop para trabajo y estudios"]
    )
    precio: float = Field(
        ...,
        gt=0,
        examples=[2499.90]
    )
    stock: int = Field(
        default=0,
        ge=0,
        examples=[10]
    )


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=500
    )
    precio: Optional[float] = Field(
        default=None,
        gt=0
    )
    stock: Optional[int] = Field(
        default=None,
        ge=0
    )


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_coleccion():
    """Valida que MongoDB se encuentre configurado."""

    if productos_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La conexión con MongoDB Atlas no está configurada."
        )

    return productos_collection


def convertir_object_id(producto_id: str) -> ObjectId:
    """Convierte un identificador de texto a ObjectId."""

    try:
        return ObjectId(producto_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El identificador del producto no es válido."
        )


def serializar_producto(documento: dict) -> dict:
    """Convierte un documento de MongoDB en una respuesta JSON."""

    return {
        "id": str(documento["_id"]),
        "nombre": documento["nombre"],
        "descripcion": documento.get("descripcion"),
        "precio": documento["precio"],
        "stock": documento.get("stock", 0)
    }


# ============================================================
# ENDPOINTS DE ESTADO
# ============================================================

@app.get("/")
def read_root():
    return {
        "mensaje": "API de Catálogo de Productos - Funcionando"
    }


@app.get("/health")
def health_check():
    """Comprueba que la API se encuentra ejecutándose."""

    return {
        "status": "healthy",
        "service": "ecommerce-api"
    }


@app.get("/ready")
def readiness_check():
    """Comprueba que la API puede comunicarse con MongoDB."""

    if mongo_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB Atlas no está configurado."
        )

    try:
        mongo_client.admin.command("ping")

        return {
            "status": "ready",
            "database": MONGODB_DB_NAME
        }

    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo establecer conexión con MongoDB Atlas."
        )


# ============================================================
# CRUD DE PRODUCTOS
# ============================================================

@app.get("/productos")
def listar_productos():
    collection = obtener_coleccion()

    documentos = collection.find().limit(100)

    return {
        "productos": [
            serializar_producto(documento)
            for documento in documentos
        ]
    }


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: str):
    collection = obtener_coleccion()
    object_id = convertir_object_id(producto_id)

    documento = collection.find_one({"_id": object_id})

    if documento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    return serializar_producto(documento)


@app.post(
    "/productos",
    status_code=status.HTTP_201_CREATED
)
def crear_producto(producto: ProductoCreate):
    collection = obtener_coleccion()

    datos = producto.model_dump()
    resultado = collection.insert_one(datos)
    documento = collection.find_one({"_id": resultado.inserted_id})

    return serializar_producto(documento)


@app.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: str,
    producto: ProductoUpdate
):
    collection = obtener_coleccion()
    object_id = convertir_object_id(producto_id)

    cambios = producto.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar al menos un campo para actualizar."
        )

    documento = collection.find_one_and_update(
        {"_id": object_id},
        {"$set": cambios},
        return_document=ReturnDocument.AFTER
    )

    if documento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    return serializar_producto(documento)


@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_producto(producto_id: str):
    collection = obtener_coleccion()
    object_id = convertir_object_id(producto_id)

    resultado = collection.delete_one({"_id": object_id})

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    return None
