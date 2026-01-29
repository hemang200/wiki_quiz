from sqlalchemy.orm import Session
from models import Article
from schemas import QuizResponse
import logging

logger = logging.getLogger(__name__)


def create_article(db: Session, data: dict) -> Article:
    """Create and store a new article with quiz in database"""
    article = Article(**data)
    db.add(article)
    db.commit()
    db.refresh(article)
    logger.info(f"✅ Stored article: {data.get('title')}")
    return article


def get_all_articles(db: Session, limit: int = 50, skip: int = 0) -> list:
    """Retrieve all articles from database with pagination"""
    return db.query(Article).offset(skip).limit(limit).order_by(Article.created_at.desc()).all()


def get_article_by_id(db: Session, article_id: int) -> Article:
    """Retrieve a specific article by ID"""
    return db.query(Article).filter(Article.id == article_id).first()


def get_article_by_url(db: Session, url: str) -> Article:
    """Check if article already exists (for caching)"""
    return db.query(Article).filter(Article.url == url).first()


def delete_article(db: Session, article_id: int) -> bool:
    """Delete an article from database"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
        logger.info(f"✅ Deleted article: {article_id}")
        return True
    return False
