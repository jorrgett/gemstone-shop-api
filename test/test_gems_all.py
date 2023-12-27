import json
import pytest
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..app.main import gem_router

# Puedes usar una configuración de prueba separada si es necesario
app = FastAPI()
app.include_router(gem_router)
load_dotenv()

# Configuración de la base de datos para pruebas
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(DATABASE_URL)

def override_get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[Session] = override_get_db
client = TestClient(app)

# Datos de prueba
test_gem_data = {
    "lte": 1000,
    "gte": 500,
    "type": ["diamond", "ruby"]
}

# Datos de prueba de usuario autenticado (si es necesario)
test_user_data = {
    "username": "testuser",
    "password": "testpassword",
    "is_seller": True  # Ajusta según tus necesidades
}

# Función de prueba
def test_get_gems():
    # Registra un usuario de prueba (si es necesario)
    response_register = client.post("/register", json=test_user_data)
    assert response_register.status_code == 200

    # Inicia sesión con el usuario de prueba (si es necesario)
    response_login = client.post("/token", data={"username": test_user_data["username"], "password": test_user_data["password"]})
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    # Realiza una solicitud GET a tu ruta con datos de prueba y token de autenticación
    response = client.get("/gems/all", params=test_gem_data, headers={"Authorization": f"Bearer {token}"})

    # Verifica que la solicitud haya sido exitosa (código de estado HTTP 200)
    assert response.status_code == 200

    # Verifica el formato de la respuesta
    assert "gems" in response.json()

    # Verifica que los datos de la respuesta sean del tipo esperado
    gems_response = response.json()["gems"]
    assert isinstance(gems_response, list)

    # Verifica que la respuesta contenga datos esperados (ajusta según tu lógica)
    for gem_data in gems_response:
        assert "gem" in gem_data
        assert "props" in gem_data
        assert "id" in gem_data["gem"]
        assert "name" in gem_data["gem"]
        assert "price" in gem_data["gem"]
        assert "gem_type" in gem_data["gem"]
        assert "cut" in gem_data["props"]
        assert "carat" in gem_data["props"]
        assert "color" in gem_data["props"]

    # Asegúrate de cerrar la conexión después de la prueba
    client.close()

# Puedes agregar más pruebas según sea necesario
