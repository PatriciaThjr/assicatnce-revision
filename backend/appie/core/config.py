# backend/appie/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Assistant Révisions"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MySQL Database - WAMP
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = "assistant_revisions"
    
    # Security
    SECRET_KEY: str = "votre_cle_secrete_pour_jwt_changez_moi_en_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Emails (même si pas encore utilisés)
    SENDER_EMAIL: Optional[str] = None
    SENDER_PASSWORD: Optional[str] = None

    # URL de la base de données (on la déclare ici → plus de problème)
    DATABASE_URL: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # Autorise les variables supplémentaires dans .env


# Instance globale
settings = Settings()

# On construit l'URL seulement si elle n'est pas déjà définie dans le .env
if not settings.DATABASE_URL:
    settings.DATABASE_URL = (
        f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
        f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
    )