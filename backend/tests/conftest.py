import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from appie.main import app
from appie.core.database import get_db
from appie.models.models import Base

@pytest.fixture(scope="session")
def test_client():
    """Client de test pour toutes les suites de tests"""
    # Base de données en mémoire pour les tests
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Nettoyage
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(test_client):
    """Créer un utilisateur de test"""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    response = test_client.post("/api/v1/users/", json=user_data)
    return response.json()