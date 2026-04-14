import logging
from typing import Optional, List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from app.config import settings

logger = logging.getLogger(__name__)

class LLMTutorService:
    """Service for AI-powered tutoring interactions"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=settings.TUTOR_TEMPERATURE,
            max_tokens=settings.TUTOR_MAX_TOKENS,
        )
        
    def create_system_prompt(self, topic: str, difficulty_level: str, context: Optional[str] = None) -> str:
        """Create a dynamic system prompt for the tutor"""
        
        difficulty_guidance = {
            "beginner": "Explain concepts in very simple, layman's terms. Use analogies and everyday examples.",
            "intermediate": "Provide balanced explanations with some technical depth. Include practical examples.",
            "advanced": "Use technical terminology. Focus on nuances, edge cases, and advanced applications."
        }
        
        base_prompt = f"""You are an expert, patient, and engaging AI tutor specialized in teaching '{topic}'. 

Your teaching style:
- Explain concepts in very simple, layman's language like a real expert tutor would
- Use relatable analogies and real-world examples
- Break down complex topics into digestible pieces
- Be conversational and encouraging
- Adapt explanations based on student responses
- Provide step-by-step guidance

Difficulty Level: {difficulty_guidance.get(difficulty_level, difficulty_guidance['intermediate'])}

Your goals:
1. Help the student understand the topic deeply
2. Answer questions clearly and patiently
3. Check for understanding by asking follow-up questions
4. Provide examples and use visualizations when needed
5. Be ready to explain things differently if the student doesn't understand

Remember: You're teaching a student, not writing a textbook. Be warm, encouraging, and use conversational language."""

        if context:
            base_prompt += f"\n\nAdditional Context:\n{context}"
            
        return base_prompt
    
    def generate_tutoring_response(
        self, 
        topic: str,
        difficulty_level: str,
        messages: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> str:
        """Generate a tutoring response based on conversation history"""
        
        try:
            system_prompt = self.create_system_prompt(topic, difficulty_level, context)
            
            # Build message history
            langchain_messages = [SystemMessage(content=system_prompt)]
            
            for msg in messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
            
            # Get response
            response = self.llm.invoke(langchain_messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating tutoring response: {str(e)}")
            raise
    
    def generate_assessment_question(
        self,
        topic: str,
        difficulty_level: str,
        previous_messages: List[Dict[str, str]],
        areas_covered: List[str]
    ) -> str:
        """Generate an assessment question to check understanding"""
        
        try:
            assessment_prompt = f"""Based on the tutoring session on '{topic}' at {difficulty_level} level, 
generate a single assessment question to check if the student understands what we've covered so far.

Topics covered so far: {', '.join(areas_covered)}

Requirements for the question:
1. Be specific to what was taught
2. Check for deep understanding, not just memorization
3. Ask them to apply the concept or explain it in their own words
4. Keep it concise (1-2 sentences)
5. Make it engaging and not intimidating

Return ONLY the question, nothing else."""

            system_prompt = "You are an expert educator creating assessment questions. Your questions are clear, fair, and check for true understanding."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=assessment_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating assessment question: {str(e)}")
            raise
    
    def evaluate_student_answer(
        self,
        topic: str,
        question: str,
        student_answer: str,
        difficulty_level: str
    ) -> Dict[str, any]:
        """Evaluate a student's answer and provide feedback"""
        
        try:
            evaluation_prompt = f"""You are an expert evaluator. A student answered a question about '{topic}' at {difficulty_level} level.

Question: {question}

Student's Answer: {student_answer}

Evaluate the answer and provide:
1. A mastery score from 0-100 (0 = no understanding, 100 = perfect understanding)
2. Constructive feedback explaining what they got right and what could be improved
3. A follow-up explanation if needed

Format your response as JSON:
{{
    "mastery_score": <0-100>,
    "feedback": "<feedback text>",
    "follow_up": "<optional follow-up explanation>"
}}

Return ONLY valid JSON, no additional text."""

            system_prompt = "You are an expert educator evaluating student responses. Be fair, encouraging, and constructive."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=evaluation_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse response
            import json
            try:
                result = json.loads(response.content)
                return result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse evaluation response: {response.content}")
                return {
                    "mastery_score": 50,
                    "feedback": "Thank you for your response. Keep practicing!",
                    "follow_up": ""
                }
            
        except Exception as e:
            logger.error(f"Error evaluating student answer: {str(e)}")
            raise
