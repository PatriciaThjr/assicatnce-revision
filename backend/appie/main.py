from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from appie.core.config import settings
from appie.api import auth, users, modules, quizzes, planning

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(modules.router, prefix=settings.API_V1_STR, tags=["modules"])
app.include_router(quizzes.router, prefix=settings.API_V1_STR, tags=["quizzes"])
app.include_router(planning.router, prefix=settings.API_V1_STR, tags=["planning"])

@app.get("/")
def read_root():
    return {"message": "Assistant de Révisions API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}