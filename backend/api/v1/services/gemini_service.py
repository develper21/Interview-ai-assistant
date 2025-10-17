"""
Enhanced Gemini AI service for interview assistance and content generation
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import google.generativeai as genai
from sqlalchemy.orm import Session

from core.config import settings
from core.models import InterviewSession, InterviewQuestion, InterviewResponse, User


class GeminiService:
    """Enhanced Gemini AI service for interview assistance"""

    def __init__(self):
        """Initialize Gemini service"""
        if not settings.google_api_key:
            raise ValueError("Google API key not configured")

        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    async def generate_interview_questions(
        self,
        skills: List[str],
        difficulty: str = "medium",
        question_count: int = 5,
        question_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate interview questions based on skills and difficulty"""

        if question_types is None:
            question_types = ["technical", "behavioral", "situational"]

        prompt = f"""
        Generate {question_count} interview questions for a {difficulty} level candidate with skills in: {', '.join(skills)}.

        Question types to include: {', '.join(question_types)}

        For each question, provide:
        1. Question text
        2. Question type (technical/behavioral/situational)
        3. Difficulty level (easy/medium/hard)
        4. Expected answer keywords/phrases
        5. AI prompt for evaluating responses

        Format the response as a JSON array of objects with keys:
        - question_text
        - question_type
        - difficulty
        - expected_answer
        - ai_prompt

        Ensure questions are relevant to the specified skills and appropriate for the difficulty level.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            # Parse JSON response
            questions_data = json.loads(response.text.strip())

            if not isinstance(questions_data, list):
                questions_data = [questions_data]

            return questions_data[:question_count]  # Limit to requested count

        except Exception as e:
            print(f"Error generating questions: {e}")
            # Fallback: return basic questions
            return [
                {
                    "question_text": f"Tell me about your experience with {skill}?",
                    "question_type": "behavioral",
                    "difficulty": difficulty,
                    "expected_answer": f"Experience with {skill}, projects, achievements",
                    "ai_prompt": f"Evaluate response about {skill} experience"
                }
                for skill in skills[:question_count]
            ]

    async def evaluate_response(
        self,
        question: str,
        user_response: str,
        expected_answer: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Evaluate user's response to an interview question"""

        context_str = ""
        if context:
            context_str = f"\nContext: {json.dumps(context)}"

        prompt = f"""
        Evaluate this interview response:

        Question: {question}
        Expected Answer: {expected_answer}
        User's Response: {user_response}{context_str}

        Provide evaluation in JSON format with:
        {{
            "score": (0-100),
            "feedback": "Detailed feedback on the response",
            "strengths": ["list", "of", "strengths"],
            "improvements": ["list", "of", "improvement areas"],
            "overall_assessment": "Brief overall assessment"
        }}

        Be constructive and specific in your feedback.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            # Parse JSON response
            evaluation_data = json.loads(response.text.strip())

            # Ensure score is within 0-100 range
            evaluation_data["score"] = max(0, min(100, evaluation_data.get("score", 50)))

            return evaluation_data

        except Exception as e:
            print(f"Error evaluating response: {e}")
            # Fallback evaluation
            return {
                "score": 70,
                "feedback": "Response received and noted.",
                "strengths": ["Provided a response"],
                "improvements": ["Could provide more specific details"],
                "overall_assessment": "Adequate response"
            }

    async def generate_suggestion(
        self,
        question: str,
        previous_responses: List[str] = None,
        user_profile: Dict[str, Any] = None
    ) -> str:
        """Generate real-time suggestion for answering a question"""

        context = ""
        if previous_responses:
            context += f"\nPrevious responses: {', '.join(previous_responses[:2])}"

        if user_profile:
            context += f"\nUser profile: {json.dumps(user_profile)}"

        prompt = f"""
        The user is being asked: "{question}"

        Provide a concise, helpful suggestion for answering this interview question.{context}

        Focus on:
        1. Key points to cover
        2. Structure for the answer
        3. Specific examples if relevant

        Keep the suggestion brief (2-3 sentences) and actionable.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            return response.text.strip()

        except Exception as e:
            print(f"Error generating suggestion: {e}")
            return "Structure your answer with specific examples and focus on your relevant experience."

    async def generate_interview_summary(
        self,
        session_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive interview summary"""

        prompt = f"""
        Analyze this interview session and provide a comprehensive summary:

        Session Data: {json.dumps(session_data, default=str)}

        Provide analysis in JSON format with:
        {{
            "overall_score": (0-100),
            "strengths": ["list", "of", "key strengths"],
            "areas_for_improvement": ["list", "of", "improvement areas"],
            "detailed_feedback": "Comprehensive feedback",
            "recommendations": ["specific", "actionable", "recommendations"],
            "skill_assessment": {{
                "strong_skills": ["skill1", "skill2"],
                "developing_skills": ["skill3", "skill4"]
            }}
        }}

        Be specific and constructive in your analysis.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            # Parse JSON response
            summary_data = json.loads(response.text.strip())

            # Ensure score is within 0-100 range
            summary_data["overall_score"] = max(0, min(100, summary_data.get("overall_score", 75)))

            return summary_data

        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback summary
            return {
                "overall_score": 75,
                "strengths": ["Completed interview session"],
                "areas_for_improvement": ["Continue practicing"],
                "detailed_feedback": "Interview session completed successfully.",
                "recommendations": ["Continue preparing for future interviews"],
                "skill_assessment": {
                    "strong_skills": [],
                    "developing_skills": []
                }
            }

    async def generate_content_ideas(
        self,
        topic: str,
        content_type: str,
        target_audience: str = "developers"
    ) -> List[str]:
        """Generate content ideas for blog posts or articles"""

        prompt = f"""
        Generate 5 creative content ideas for {content_type} about "{topic}" targeted at {target_audience}.

        Each idea should be:
        - Specific and actionable
        - Include a compelling title
        - Be relevant to current industry trends
        - Provide value to the target audience

        Format as a JSON array of objects with "title" and "description" keys.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            ideas_data = json.loads(response.text.strip())

            if not isinstance(ideas_data, list):
                ideas_data = [ideas_data]

            return ideas_data[:5]

        except Exception as e:
            print(f"Error generating content ideas: {e}")
            return [
                {
                    "title": f"Getting Started with {topic}",
                    "description": f"A beginner's guide to {topic} for {target_audience}"
                }
            ]

    async def analyze_user_progress(
        self,
        user_data: Dict[str, Any],
        recent_sessions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze user progress and provide insights"""

        prompt = f"""
        Analyze this user's interview performance data and provide insights:

        User Profile: {json.dumps(user_data, default=str)}
        Recent Sessions: {json.dumps(recent_sessions, default=str)}

        Provide analysis in JSON format with:
        {{
            "progress_trend": "upward/downward/stable",
            "strengths": ["consistent strengths"],
            "improvement_areas": ["areas needing work"],
            "milestones": ["achievements to celebrate"],
            "next_steps": ["actionable next steps"],
            "overall_assessment": "Brief overall assessment"
        }}

        Focus on trends, improvements, and specific recommendations.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            return json.loads(response.text.strip())

        except Exception as e:
            print(f"Error analyzing progress: {e}")
            return {
                "progress_trend": "stable",
                "strengths": ["Active participation"],
                "improvement_areas": ["Continue practicing"],
                "milestones": ["Completed interview sessions"],
                "next_steps": ["Continue regular practice"],
                "overall_assessment": "Making steady progress"
            }

    async def generate_follow_up_questions(
        self,
        current_question: str,
        user_response: str,
        interview_context: Dict[str, Any] = None
    ) -> List[str]:
        """Generate follow-up questions based on user's response"""

        context_str = ""
        if interview_context:
            context_str = f"\nInterview Context: {json.dumps(interview_context)}"

        prompt = f"""
        Based on this interview exchange:

        Question: {current_question}
        Response: {user_response}{context_str}

        Generate 2-3 thoughtful follow-up questions that:
        1. Dig deeper into the user's experience
        2. Explore related technical concepts
        3. Assess problem-solving abilities

        Return as a JSON array of question strings.
        """

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )

            questions_data = json.loads(response.text.strip())

            if not isinstance(questions_data, list):
                questions_data = [questions_data]

            return questions_data[:3]

        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            return [
                "Can you elaborate on that experience?",
                "What challenges did you face in that project?",
                "How would you approach a similar situation now?"
            ]


# Global service instance
gemini_service = None

def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global gemini_service
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except ValueError:
            # Return a mock service if API key not configured
            gemini_service = MockGeminiService()
    return gemini_service


class MockGeminiService:
    """Mock Gemini service for testing when API key not available"""

    async def generate_interview_questions(self, *args, **kwargs):
        return [
            {
                "question_text": "Tell me about yourself",
                "question_type": "behavioral",
                "difficulty": "easy",
                "expected_answer": "Background, experience, interests",
                "ai_prompt": "Evaluate personal introduction"
            }
        ]

    async def evaluate_response(self, *args, **kwargs):
        return {
            "score": 75,
            "feedback": "Good response structure",
            "strengths": ["Clear communication"],
            "improvements": ["More specific examples"],
            "overall_assessment": "Solid response"
        }

    async def generate_suggestion(self, *args, **kwargs):
        return "Structure your answer with specific examples"

    async def generate_interview_summary(self, *args, **kwargs):
        return {
            "overall_score": 75,
            "strengths": ["Good communication"],
            "areas_for_improvement": ["Technical depth"],
            "detailed_feedback": "Good overall performance",
            "recommendations": ["Continue practicing"],
            "skill_assessment": {"strong_skills": [], "developing_skills": []}
        }

    async def generate_content_ideas(self, *args, **kwargs):
        return [{"title": "Getting Started", "description": "Basic guide"}]

    async def analyze_user_progress(self, *args, **kwargs):
        return {"progress_trend": "stable", "strengths": [], "improvements": []}

    async def generate_follow_up_questions(self, *args, **kwargs):
        return ["Can you elaborate?", "What challenges did you face?"]
