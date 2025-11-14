import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from appie.main import app
from appie.core.database import get_db
from appie.core.security import get_password_hash
from appie.models.models import Base, User

# Base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables de test
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    """Test l'inscription d'un nouvel utilisateur"""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user():
    """Test la connexion d'un utilisateur"""
    # D'abord créer un utilisateur
    client.post(
        "/api/v1/users/",
        json={
            "email": "login@test.com",
            "full_name": "Login Test",
            "password": "password123"
        }
    )
    
    # Puis tester le login
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "login@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test la connexion avec un mauvais mot de passe"""
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_protected_route_without_token():
    """Test l'accès à une route protégée sans token"""
    response = client.get("/api/v1/users/some-user-id")
    assert response.status_code == 401

# Nettoyage après les tests
def teardown_module(module):
    # Supprimer la base de données de test
    import os
    if os.path.exists("test.db"):
        os.remove("test.db")