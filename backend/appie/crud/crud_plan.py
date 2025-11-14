from sqlalchemy.orm import Session
from appie.models.models import StudyPlan

def create_study_plan(db: Session, user_id: str, schedule: list):
    db_plan = StudyPlan(user_id=user_id, schedule=schedule)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_user_plans(db: Session, user_id: str):
    return db.query(StudyPlan).filter(StudyPlan.user_id == user_id).all()