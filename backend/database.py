from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Using SQLite for easy setup (can switch to PostgreSQL later)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./wikiquiz.db"
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    """Dependency for FastAPI to inject database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
