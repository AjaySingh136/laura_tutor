from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.schemas import (
    TutorSessionCreate, TutorSessionResponse, ChatRequest, ChatResponse,
    MessageResponse, YouTubeURLRequest, AssessmentAnswerRequest
)
from app.models import TutorSession, SessionMessage, User, AssessmentQuestion
from app.services.llm_service import LLMTutorService
from app.services.youtube_service import YouTubeService
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", tags=["tutoring"])

# Initialize services
llm_service = LLMTutorService()
youtube_service = YouTubeService()

# Temporary: Create or get demo user (for MVP testing)
def get_or_create_demo_user(db: Session) -> User:
    user = db.query(User).filter(User.username == "demo").first()
    if not user:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = User(
            id=str(uuid.uuid4()),
            email="demo@example.com",
            username="demo",
            hashed_password=pwd_context.hash("demo123"),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@router.post("/sessions", response_model=TutorSessionResponse)
async def create_tutoring_session(
    session_data: TutorSessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new tutoring session"""
    try:
        # Get or create demo user for MVP
        user = get_or_create_demo_user(db)
        
        transcript = None
        if session_data.youtube_url:
            logger.info(f"Extracting transcript from YouTube: {session_data.youtube_url}")
            transcript = youtube_service.get_transcript(session_data.youtube_url)
            if not transcript:
                logger.warning("Could not extract transcript from YouTube URL")
        
        session = TutorSession(
            id=str(uuid.uuid4()),
            user_id=user.id,
            topic=session_data.topic,
            difficulty_level=session_data.difficulty_level,
            youtube_url=session_data.youtube_url,
            transcript=transcript,
            enable_assessment=session_data.enable_assessment,
            status="active"
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"Created tutoring session: {session.id}")
        return session
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=TutorSessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get a tutoring session"""
    session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat_with_tutor(
    session_id: str,
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Send a message to the tutor and get a response"""
    try:
        session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get previous messages
        messages = db.query(SessionMessage).filter(
            SessionMessage.session_id == session_id
        ).order_by(SessionMessage.sequence_number).all()
        
        # Convert to format for LLM
        previous_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Get context from YouTube transcript if available
        context = session.transcript[:1000] if session.transcript else None
        
        # Generate response from tutor
        tutor_response = llm_service.generate_tutoring_response(
            topic=session.topic,
            difficulty_level=session.difficulty_level,
            messages=previous_messages + [{"role": "user", "content": chat_request.message}],
            context=context
        )
        
        # Save user message
        user_msg_sequence = len(messages) + 1
        user_msg = SessionMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content=chat_request.message,
            sequence_number=user_msg_sequence,
            message_type="text"
        )
        db.add(user_msg)
        
        # Save assistant message
        assistant_msg_sequence = user_msg_sequence + 1
        assistant_msg = SessionMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=tutor_response,
            sequence_number=assistant_msg_sequence,
            message_type="text"
        )
        db.add(assistant_msg)
        
        # Check if we should ask an assessment question
        assessment_question = None
        if session.enable_assessment and (assistant_msg_sequence % (session.assessment_frequency or 3)) == 0:
            # Get topics covered so far
            areas_covered = [f"Message {i}" for i in range(1, assistant_msg_sequence)]
            
            assessment_question = llm_service.generate_assessment_question(
                topic=session.topic,
                difficulty_level=session.difficulty_level,
                previous_messages=previous_messages + [
                    {"role": "user", "content": chat_request.message},
                    {"role": "assistant", "content": tutor_response}
                ],
                areas_covered=areas_covered[:3]  # Last 3 areas covered
            )
            
            # Save assessment question to database
            assessment = AssessmentQuestion(
                id=str(uuid.uuid4()),
                session_id=session_id,
                question=assessment_question
            )
            db.add(assessment)
            session.assessment_count += 1
        
        session.updated_at = datetime.utcnow()
        db.commit()
        
        return ChatResponse(
            user_message=chat_request.message,
            tutor_response=tutor_response,
            message_type="text",
            assessment_question=assessment_question
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get all messages in a session"""
    messages = db.query(SessionMessage).filter(
        SessionMessage.session_id == session_id
    ).order_by(SessionMessage.sequence_number).all()
    return messages

@router.post("/sessions/{session_id}/assessment/{question_id}/answer")
async def submit_assessment_answer(
    session_id: str,
    question_id: str,
    request: AssessmentAnswerRequest,
    db: Session = Depends(get_db)
):
    """Submit an answer to an assessment question"""
    try:
        session = db.query(TutorSession).filter(TutorSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        assessment = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == question_id
        ).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Evaluate the answer
        evaluation = llm_service.evaluate_student_answer(
            topic=session.topic,
            question=assessment.question,
            student_answer=request.answer,
            difficulty_level=session.difficulty_level
        )
        
        # Save assessment result
        assessment.student_answer = request.answer
        assessment.ai_evaluation = evaluation.get("feedback", "")
        assessment.mastery_score = evaluation.get("mastery_score", 50)
        assessment.answered_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "question_id": question_id,
            "mastery_score": evaluation.get("mastery_score"),
            "feedback": evaluation.get("feedback"),
            "follow_up": evaluation.get("follow_up", "")
        }
        
    except Exception as e:
        logger.error(f"Error submitting assessment: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/youtube/transcript")
async def get_youtube_transcript(
    request: YouTubeURLRequest
):
    """Extract transcript from a YouTube URL"""
    try:
        transcript = youtube_service.get_transcript(request.url)
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="Could not extract transcript. Video might not have captions."
            )
        
        return {
            "success": True,
            "transcript": transcript,
            "length": len(transcript)
        }
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
