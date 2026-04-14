from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("TutorSession", back_populates="user", cascade="all, delete-orphan")
    
class TutorSession(Base):
    __tablename__ = "tutor_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    topic = Column(String, index=True)
    difficulty_level = Column(String, default="intermediate")  # beginner, intermediate, advanced
    youtube_url = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    enable_assessment = Column(Boolean, default=True)
    assessment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="active")  # active, completed, paused
    metadata = Column(JSON, nullable=True)  # Store additional session data
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("SessionMessage", back_populates="session", cascade="all, delete-orphan")
    assessments = relationship("AssessmentQuestion", back_populates="session", cascade="all, delete-orphan")
    
class SessionMessage(Base):
    __tablename__ = "session_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("tutor_sessions.id"))
    role = Column(String)  # user, assistant, system
    content = Column(Text)
    message_type = Column(String, default="text")  # text, image, video, code, assessment
    metadata = Column(JSON, nullable=True)  # Store image URLs, code snippets, etc
    sequence_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("TutorSession", back_populates="messages")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("tutor_sessions.id"))
    question = Column(Text)
    student_answer = Column(Text, nullable=True)
    ai_evaluation = Column(Text, nullable=True)
    mastery_score = Column(Float, nullable=True)  # 0-100
    asked_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)
    
    # Relationships
    session = relationship("TutorSession", back_populates="assessments")
