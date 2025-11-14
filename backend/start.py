import uvicorn
from fastapi import FastAPI

# Création directe de l'app si l'import échoue
try:
    from appie.main import app
except ImportError:
    # Fallback: créer une app basique
    app = FastAPI(title="Assistant Révisions Fallback")
    
    @app.get("/")
    async def root():
        return {"message": "Application en mode fallback"}

if __name__ == "__main__":
    uvicorn.run(
        "start:app",  # Référence à l'app dans ce fichier
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )