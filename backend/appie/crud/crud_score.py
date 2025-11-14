from sqlalchemy.orm import Session
from appie.models.models import Score

def get_user_scores(db: Session, user_id: str):
    return db.query(Score).filter(Score.user_id == user_id).all()

def get_module_scores(db: Session, module_id: str):
    return db.query(Score).filter(Score.module_id == module_id).all()