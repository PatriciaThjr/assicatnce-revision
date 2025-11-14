from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from appie.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    modules = relationship("Module", back_populates="user", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="user", cascade="all, delete-orphan")
    plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    weekly_objectives = Column(JSON)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="modules")
    quizzes = relationship("Quiz", back_populates="module", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="module", cascade="all, delete-orphan")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    questions = Column(JSON)
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    module = relationship("Module", back_populates="quizzes")
    scores = relationship("Score", back_populates="quiz", cascade="all, delete-orphan")

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    value = Column(Float, nullable=False)
    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    quiz = relationship("Quiz", back_populates="scores")
    user = relationship("User", back_populates="scores")
    module = relationship("Module", back_populates="scores")

class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    schedule = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="plans")