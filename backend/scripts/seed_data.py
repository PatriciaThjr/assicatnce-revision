from appie.core.database import SessionLocal
from appie.models.models import User, Module, Quiz
from appie.core.security import get_password_hash

def seed_database():
    db = SessionLocal()
    
    try:
        # Créer un utilisateur de test
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Créer des modules de test
        modules_data = [
            {
                "name": "Mathématiques",
                "description": "Cours de mathématiques avancées",
                "weekly_objectives": ["Algèbre", "Géométrie", "Calcul"]
            },
            {
                "name": "Physique",
                "description": "Cours de physique fondamentale",
                "weekly_objectives": ["Mécanique", "Électricité", "Optique"]
            }
        ]
        
        for module_data in modules_data:
            module = Module(**module_data, user_id=user.id)
            db.add(module)
        
        db.commit()
        print("✅ Données de test créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.roll