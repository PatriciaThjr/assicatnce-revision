from sqlalchemy.orm import Session
from appie.models.models import Quiz, Score
from appie.schemas.schemas import QuizCreate
from typing import Dict

def create_quiz(db: Session, quiz: QuizCreate):
    db_quiz = Quiz(
        title=quiz.title,
        questions=[q.dict() for q in quiz.questions],
        module_id=quiz.module_id
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def get_module_quizzes(db: Session, module_id: str):
    return db.query(Quiz).filter(Quiz.module_id == module_id).all()

def calculate_score(db: Session, quiz_id: str, submission: Dict):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise ValueError("Quiz non trouvé")
    
    correct_answers = 0
    for question in quiz.questions:
        user_answer = submission['answers'].get(question['id'])
        if user_answer == question['correct_answer']:
            correct_answers += 1
    
    score_value = correct_answers / len(quiz.questions) if quiz.questions else 0
    
    db_score = Score(
        value=score_value,
        quiz_id=quiz_id,
        user_id=submission['user_id'],
        module_id=quiz.module_id
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score