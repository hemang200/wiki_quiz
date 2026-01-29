from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base


class Article(Base):
    """Database model for storing Wikipedia articles and generated quizzes"""
    
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    key_entities = Column(JSON, nullable=True)  # {"people": [], "organizations": [], "locations": []}
    sections = Column(JSON)  # List of section titles
    quiz = Column(JSON)  # List of quiz questions
    related_topics = Column(JSON)  # List of related topics
    raw_html = Column(Text, nullable=True)  # Optional: store raw HTML for reference
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class Config:
        arbitrary_types_allowed = True
