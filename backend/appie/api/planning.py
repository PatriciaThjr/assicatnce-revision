from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from appie.core.database import get_db
from appie.schemas.schemas import StudySession
from appie.algorithms.planning_generator import PlanningGenerator

router = APIRouter()

@router.post("/planning/generate", response_model=List[StudySession])
def generate_study_plan(
    user_id: str,
    rules: dict,
    db: Session = Depends(get_db)
):
    generator = PlanningGenerator(db)
    plan = generator.generate_study_plan(user_id, rules)
    return plan