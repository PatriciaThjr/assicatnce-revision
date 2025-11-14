import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from appie.main import app
from appie.core.database import get_db
from appie.models.models import Base, User, Module, Score, Quiz

# Configuration base de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_planning.db"
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

class TestPlanning:
    @classmethod
    def setup_class(cls):
        """Setup avant tous les tests"""
        # Créer utilisateur
        user_response = client.post("/api/v1/users/", json={
            "email": "planning@test.com",
            "full_name": "Planning Test User",
            "password": "password123"
        })
        cls.user_id = user_response.json()["id"]
        
        # Créer modules avec différents niveaux de performance
        cls.modules = {}
        
        # Module avec faible score (haute priorité)
        module1_response = client.post(
            f"/api/v1/modules/?user_id={cls.user_id}",
            json={
                "name": "Mathématiques Faibles",
                "description": "Module avec scores faibles",
                "weekly_objectives": ["Algèbre", "Calcul"]
            }
        )
        cls.modules["weak"] = module1_response.json()["id"]
        
        # Module avec score moyen
        module2_response = client.post(
            f"/api/v1/modules/?user_id={cls.user_id}",
            json={
                "name": "Physique Moyenne",
                "description": "Module avec scores moyens",
                "weekly_objectives": ["Mécanique", "Optique"]
            }
        )
        cls.modules["medium"] = module2_response.json()["id"]
        
        # Module avec bon score (basse priorité)
        module3_response = client.post(
            f"/api/v1/modules/?user_id={cls.user_id}",
            json={
                "name": "Chimie Forte",
                "description": "Module avec bons scores",
                "weekly_objectives": ["Organique", "Analytique"]
            }
        )
        cls.modules["strong"] = module3_response.json()["id"]
        
        # Créer des quiz et scores pour simuler les performances
        cls._create_test_scores()

    @classmethod
    def _create_test_scores(cls):
        """Créer des scores de test pour chaque module"""
        # Scores faibles pour Mathématiques (0.4, 0.3)
        cls._create_quiz_and_score(cls.modules["weak"], 0.4)
        cls._create_quiz_and_score(cls.modules["weak"], 0.3)
        
        # Scores moyens pour Physique (0.7, 0.6)
        cls._create_quiz_and_score(cls.modules["medium"], 0.7)
        cls._create_quiz_and_score(cls.modules["medium"], 0.6)
        
        # Scores forts pour Chimie (0.9, 0.85)
        cls._create_quiz_and_score(cls.modules["strong"], 0.9)
        cls._create_quiz_and_score(cls.modules["strong"], 0.85)

    @classmethod
    def _create_quiz_and_score(cls, module_id, score_value):
        """Créer un quiz et un score associé"""
        # Créer un quiz
        quiz_response = client.post("/api/v1/quizzes/", json={
            "title": f"Quiz Test {module_id}",
            "module_id": module_id,
            "questions": [
                {
                    "id": "1",
                    "text": "Question test",
                    "type": "multiple_choice",
                    "options": ["A", "B", "C"],
                    "correct_answer": "A"
                }
            ]
        })
        quiz_id = quiz_response.json()["id"]
        
        # Simuler un score (normalement fait via soumission de quiz)
        # Pour les tests, on utilise directement l'endpoint de soumission
        submission = {
            "user_id": cls.user_id,
            "answers": {"1": "A"} if score_value > 0.5 else {"1": "B"}
        }
        # Ajuster pour obtenir le score désiré
        if score_value == 0.4:
            submission = {"user_id": cls.user_id, "answers": {"1": "B"}}
        
        client.post(f"/api/v1/quizzes/{quiz_id}/submit", json=submission)

    def test_generate_planning_basic(self):
        """Test la génération basique d'un planning"""
        rules = {
            "sessions_per_week": 5,
            "session_duration": 60
        }
        
        response = client.post(
            f"/api/v1/planning/generate?user_id={self.user_id}",
            json=rules
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Vérifier que le planning est généré
        assert len(data) > 0
        assert isinstance(data, list)
        
        # Vérifier la structure des sessions
        session = data[0]
        assert "module_id" in session
        assert "module_name" in session
        assert "date" in session
        assert "duration" in session
        assert "objectives" in session
        assert "priority" in session

    def test_planning_prioritizes_weak_modules(self):
        """Test que les modules faibles sont prioritaires"""
        rules = {
            "sessions_per_week": 3,
            "session_duration": 60
        }
        
        response = client.post(
            f"/api/v1/planning/generate?user_id={self.user_id}",
            json=rules
        )
        
        data = response.json()
        
        # Les premières sessions devraient être pour le module faible
        weak_module_sessions = [s for s in data[:3] if s["module_id"] == self.modules["weak"]]
        strong_module_sessions = [s for s in data[:3] if s["module_id"] == self.modules["strong"]]
        
        # Il devrait y avoir plus de sessions pour les modules faibles
        assert len(weak_module_sessions) >= len(strong_module_sessions)

    def test_planning_session_structure(self):
        """Test la structure d'une session de planning"""
        rules = {
            "sessions_per_week": 1,
            "session_duration": 90
        }
        
        response = client.post(
            f"/api/v1/planning/generate?user_id={self.user_id}",
            json=rules
        )
        
        data = response.json()
        session = data[0]
        
        # Vérifications de structure
        assert session["duration"] == 90
        assert isinstance(session["objectives"], list)
        assert len(session["objectives"]) > 0
        assert session["priority"] in ["high", "medium", "low"]
        
        # Vérifier que la date est dans le futur
        session_date = datetime.fromisoformat(session["date"].replace('Z', '+00:00'))
        assert session_date > datetime.utcnow()

    def test_planning_with_different_rules(self):
        """Test avec différentes configurations de règles"""
        test_cases = [
            {"sessions_per_week": 2, "session_duration": 30},
            {"sessions_per_week": 7, "session_duration": 120},
            {"sessions_per_week": 4, "session_duration": 45}
        ]
        
        for rules in test_cases:
            response = client.post(
                f"/api/v1/planning/generate?user_id={self.user_id}",
                json=rules
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Vérifier que la durée est respectée
            assert data[0]["duration"] == rules["session_duration"]
            
            # Vérifier qu'il y a le bon nombre de sessions sur 15 semaines
            total_sessions = rules["sessions_per_week"] * 15
            assert len(data) == total_sessions

    def test_planning_no_scores(self):
        """Test avec un utilisateur sans scores"""
        # Créer un nouvel utilisateur sans scores
        new_user_response = client.post("/api/v1/users/", json={
            "email": "new@test.com",
            "full_name": "New Test User",
            "password": "password123"
        })
        new_user_id = new_user_response.json()["id"]
        
        rules = {
            "sessions_per_week": 3,
            "session_duration": 60
        }
        
        response = client.post(
            f"/api/v1/planning/generate?user_id={new_user_id}",
            json=rules
        )
        
        # Devrait quand même fonctionner (planning vide ou par défaut)
        assert response.status_code == 200
        data = response.json()
        # Peut retourner une liste vide ou un planning par défaut

    @classmethod
    def teardown_class(cls):
        """Nettoyage après les tests"""
        import os
        if os.path.exists("test_planning.db"):
            os.remove("test_planning.db")