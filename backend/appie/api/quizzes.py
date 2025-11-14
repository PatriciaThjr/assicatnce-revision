from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from appie.core.database import get_db
from appie.schemas.schemas import Quiz, QuizCreate, Score
from appie.crud.crud_quiz import create_quiz, get_module_quizzes, calculate_score

router = APIRouter()

@router.post("/quizzes/", response_model=Quiz)
def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz(db=db, quiz=quiz)

@router.get("/modules/{module_id}/quizzes", response_model=List[Quiz])
def read_module_quizzes(module_id: str, db: Session = Depends(get_db)):
    return get_module_quizzes(db, module_id=module_id)

@router.post("/quizzes/{quiz_id}/submit", response_model=Score)
def submit_quiz_answer(
    quiz_id: str, 
    submission: Dict,
    db: Session = Depends(get_db)
):
    return calculate_score(db=db, quiz_id=quiz_id, submission=submission)