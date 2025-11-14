from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    weekly_objectives: Optional[List[str]] = None

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Question(BaseModel):
    id: str
    text: str
    type: str
    options: Optional[List[str]] = None
    correct_answer: str

class QuizBase(BaseModel):
    title: str
    questions: List[Question]

class QuizCreate(QuizBase):
    module_id: str

class Quiz(QuizBase):
    id: str
    module_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScoreBase(BaseModel):
    value: float
    quiz_id: str
    module_id: str

class ScoreCreate(ScoreBase):
    pass

class Score(ScoreBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudySession(BaseModel):
    module_id: str
    module_name: str
    date: datetime
    duration: int
    objectives: List[str]
    priority: str

class StudyPlanBase(BaseModel):
    schedule: List[StudySession]

class StudyPlan(StudyPlanBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None