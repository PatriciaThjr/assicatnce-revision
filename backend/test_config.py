# backend/test_config.py
try:
    import pytest
    from appie.core.config import settings
    print("✅ Configuration importée avec succès!")
    print(f"📊 Base de données: {settings.MYSQL_DB}")
    print(f"🔗 URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("🔧 Vérifiez l'installation de Pydantic")