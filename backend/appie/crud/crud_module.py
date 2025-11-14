from sqlalchemy.orm import Session
from appie.models.models import Module
from appie.schemas.schemas import ModuleCreate

def get_user_modules(db: Session, user_id: str):
    return db.query(Module).filter(Module.user_id == user_id).all()

def get_module(db: Session, module_id: str):
    return db.query(Module).filter(Module.id == module_id).first()

def create_user_module(db: Session, module: ModuleCreate, user_id: str):
    db_module = Module(**module.dict(), user_id=user_id)
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module