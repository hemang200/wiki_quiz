from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question: str
    options: List[str]
    answer: str
    difficulty: str  # "easy", "medium", "hard"
    explanation: str


class KeyEntities(BaseModel):
    """Schema for extracted named entities"""
    people: Optional[List[str]] = []
    organizations: Optional[List[str]] = []
    locations: Optional[List[str]] = []


class QuizResponse(BaseModel):
    """Schema for API response when generating/retrieving a quiz"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Optional[KeyEntities] = None
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    created_at: Optional[datetime] = None


class QuizHistoryItem(BaseModel):
    """Schema for history table display"""
    id: int
    url: str
    title: str
    created_at: Optional[datetime] = None


class GenerateQuizRequest(BaseModel):
    """Schema for requesting quiz generation"""
    url: str
