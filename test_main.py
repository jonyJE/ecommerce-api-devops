import mongomock
import pytest
from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def configurar_mongodb_simulado(monkeypatch):
    """
    Crea una base MongoDB temporal para cada prueba.

    Las pruebas nunca utilizan la contraseña ni el clúster real
    de MongoDB Atlas.
    """

    mongo_client_mock = mongomock.MongoClient()
    database_mock = mongo_client_mock["ecommerce"]
    collection_mock = database_mock["productos"]

    monkeypatch.setattr(
        main,
        "mongo_client",
        mongo_client_mock
    )
    monkeypatch.setattr(
        main,
        "database",
        database_mock
    )
    monkeypatch.setattr(
        main,
        "productos_collection",
        collection_mock
    )

    yield


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "mensaje": "API de Catálogo de Productos - Funcionando"
    }


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "ecommerce-api"
    }


def test_crud_completo_productos():
    producto = {
        "nombre": "Laptop de prueba",
        "descripcion": "Producto creado durante el test",
        "precio": 2500.00,
        "stock": 10
    }

    # Crear
    response_create = client.post(
        "/productos",
        json=producto
    )

    assert response_create.status_code == 201
    producto_creado = response_create.json()
    producto_id = producto_creado["id"]

    assert producto_creado["nombre"] == "Laptop de prueba"
    assert producto_creado["stock"] == 10

    # Listar
    response_list = client.get("/productos")

    assert response_list.status_code == 200
    assert len(response_list.json()["productos"]) == 1

    # Consultar por identificador
    response_get = client.get(
        f"/productos/{producto_id}"
    )

    assert response_get.status_code == 200
    assert response_get.json()["id"] == producto_id

    # Actualizar
    response_update = client.put(
        f"/productos/{producto_id}",
        json={
            "precio": 2300.00,
            "stock": 15
        }
    )

    assert response_update.status_code == 200
    assert response_update.json()["precio"] == 2300.00
    assert response_update.json()["stock"] == 15

    # Eliminar
    response_delete = client.delete(
        f"/productos/{producto_id}"
    )

    assert response_delete.status_code == 204

    # Confirmar que fue eliminado
    response_not_found = client.get(
        f"/productos/{producto_id}"
    )

    assert response_not_found.status_code == 404


def test_precio_negativo_no_permitido():
    response = client.post(
        "/productos",
        json={
            "nombre": "Producto inválido",
            "descripcion": "Precio negativo",
            "precio": -100,
            "stock": 5
        }
    )

    assert response.status_code == 422


def test_identificador_invalido():
    response = client.get(
        "/productos/identificador-invalido"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "El identificador del producto no es válido."
    )
