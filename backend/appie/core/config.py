# backend/app/core/config.py
from pydantic_settings import BaseSettings

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
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Construire l'URL de la base de données
settings = Settings()
settings.DATABASE_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"