import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from appie.main import app
from appie.core.database import get_db
from appie.models.models import Base, User, Module, Quiz

# Configuration base de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_quiz.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Données de test
test_user = {
    "email": "quiz@test.com",
    "full_name": "Quiz Test User",
    "password": "password123"
}

test_module = {
    "name": "Mathématiques Test",
    "description": "Module de test pour les quiz",
    "weekly_objectives": ["Algèbre", "Géométrie"]
}

test_quiz = {
    "title": "Quiz de test Mathématiques",
    "module_id": "",  # Sera rempli après création du module
    "questions": [
        {
            "id": "1",
            "text": "Quel est le résultat de 2 + 2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        },
        {
            "id": "2",
            "text": "La terre est plate?",
            "type": "true_false",
            "options": ["Vrai", "Faux"],
            "correct_answer": "Faux"
        }
    ]
}

class TestQuiz:
    @classmethod
    def setup_class(cls):
        """Setup avant tous les tests de la classe"""
        # Créer un utilisateur
        user_response = client.post("/api/v1/users/", json=test_user)
        cls.user_id = user_response.json()["id"]
        
        # Créer un module
        module_response = client.post(
            f"/api/v1/modules/?user_id={cls.user_id}", 
            json=test_module
        )
        cls.module_id = module_response.json()["id"]
        
        # Mettre à jour le quiz avec le vrai module_id
        test_quiz["module_id"] = cls.module_id

    def test_create_quiz(self):
        """Test la création d'un quiz"""
        response = client.post("/api/v1/quizzes/", json=test_quiz)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_quiz["title"]
        assert len(data["questions"]) == 2
        self.quiz_id = data["id"]

    def test_get_module_quizzes(self):
        """Test la récupération des quiz d'un module"""
        response = client.get(f"/api/v1/modules/{self.module_id}/quizzes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["module_id"] == self.module_id

    def test_submit_quiz_correct_answers(self):
        """Test la soumission d'un quiz avec bonnes réponses"""
        submission = {
            "user_id": self.user_id,
            "answers": {
                "1": "4",  # Bonne réponse
                "2": "Faux"  # Bonne réponse
            }
        }
        response = client.post(f"/api/v1/quizzes/{self.quiz_id}/submit", json=submission)
        assert response.status_code == 200
        data = response.json()
        assert data["value"] == 1.0  # Score parfait
        assert data["user_id"] == self.user_id

    def test_submit_quiz_wrong_answers(self):
        """Test la soumission d'un quiz avec mauvaises réponses"""
        submission = {
            "user_id": self.user_id,
            "answers": {
                "1": "3",  # Mauvaise réponse
                "2": "Vrai"  # Mauvaise réponse
            }
        }
        response = client.post(f"/api/v1/quizzes/{self.quiz_id}/submit", json=submission)
        assert response.status_code == 200
        data = response.json()
        assert data["value"] == 0.0  # Score 0%

    def test_submit_quiz_partial_answers(self):
        """Test la soumission avec réponses partielles"""
        submission = {
            "user_id": self.user_id,
            "answers": {
                "1": "4",  # Bonne réponse
                "2": "Vrai"  # Mauvaise réponse
            }
        }
        response = client.post(f"/api/v1/quizzes/{self.quiz_id}/submit", json=submission)
        assert response.status_code == 200
        data = response.json()
        assert data["value"] == 0.5  # Score 50%

    def test_submit_quiz_missing_user_id(self):
        """Test la soumission sans user_id"""
        submission = {
            "answers": {
                "1": "4",
                "2": "Faux"
            }
        }
        response = client.post(f"/api/v1/quizzes/{self.quiz_id}/submit", json=submission)
        # Devrait échouer car user_id manquant
        assert response.status_code == 422

    @classmethod
    def teardown_class(cls):
        """Nettoyage après tous les tests"""
        import os
        if os.path.exists("test_quiz.db"):
            os.remove("test_quiz.db")