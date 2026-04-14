from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Session Schemas
class TutorSessionCreate(BaseModel):
    topic: str
    difficulty_level: Optional[str] = "intermediate"
    youtube_url: Optional[str] = None
    enable_assessment: Optional[bool] = True

class TutorSessionUpdate(BaseModel):
    difficulty_level: Optional[str] = None
    status: Optional[str] = None
    enable_assessment: Optional[bool] = None

class TutorSessionResponse(BaseModel):
    id: str
    user_id: str
    topic: str
    difficulty_level: str
    youtube_url: Optional[str]
    enable_assessment: bool
    status: str
    assessment_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    content: str
    message_type: Optional[str] = "text"
    metadata: Optional[dict] = None

class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    message_type: str
    sequence_number: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    user_message: str
    tutor_response: str
    message_type: str
    assessment_question: Optional[str] = None
    metadata: Optional[dict] = None

# Assessment Schemas
class AssessmentQuestionResponse(BaseModel):
    id: str
    question: str
    student_answer: Optional[str]
    ai_evaluation: Optional[str]
    mastery_score: Optional[float]
    asked_at: datetime
    
    class Config:
        from_attributes = True

class AssessmentAnswerRequest(BaseModel):
    question_id: str
    answer: str

# YouTube Integration
class YouTubeURLRequest(BaseModel):
    url: str

class YouTubeTranscriptResponse(BaseModel):
    transcript: str
    duration: int
    title: str
