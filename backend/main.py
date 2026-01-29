from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our modules
from scraper import scrape_wikipedia, extract_key_entities
from llm import generate_quiz
from schemas import QuizResponse, QuizHistoryItem, GenerateQuizRequest

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create data directory
DATA_DIR = Path("../data")
DATA_DIR.mkdir(exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Wiki Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ HELPER FUNCTIONS ============

def save_quiz(data: dict) -> dict:
    """Save quiz to JSON file and return with ID"""
    quiz_id = len(list(DATA_DIR.glob("quiz_*.json"))) + 1
    data["id"] = quiz_id
    data["created_at"] = datetime.now().isoformat()
    
    file_path = DATA_DIR / f"quiz_{quiz_id}.json"
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"✅ Saved quiz {quiz_id}")
    return data


def get_all_quizzes() -> list:
    """Load all quizzes from files"""
    quizzes = []
    for file in sorted(DATA_DIR.glob("quiz_*.json"), reverse=True):
        with open(file) as f:
            quizzes.append(json.load(f))
    return quizzes


def get_quiz_by_id(quiz_id: int) -> dict:
    """Load a specific quiz by ID"""
    file_path = DATA_DIR / f"quiz_{quiz_id}.json"
    if not file_path.exists():
        return None
    
    with open(file_path) as f:
        return json.load(f)


def quiz_exists_for_url(url: str) -> dict:
    """Check if quiz already exists for URL"""
    for file in DATA_DIR.glob("quiz_*.json"):
        with open(file) as f:
            quiz = json.load(f)
            if quiz.get("url") == url:
                return quiz
    return None


# ============ ENDPOINTS ============

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "✅ Wiki Quiz API is running"}


@app.post("/api/generate-quiz")
async def generate_quiz_endpoint(request: GenerateQuizRequest):
    """
    Generate a quiz from a Wikipedia article URL
    
    Steps:
    1. Check if URL already processed (caching)
    2. Scrape Wikipedia article
    3. Send to Gemini AI for quiz generation
    4. Store in database
    5. Return JSON response
    """
    url = request.url.strip()
    
    # Validate URL
    if not url.startswith("https://en.wikipedia.org/wiki/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid Wikipedia URL. Must be https://en.wikipedia.org/wiki/..."
        )
    
    try:
        # Check if already processed (caching)
        existing = quiz_exists_for_url(url)
        if existing:
            logger.info(f"📦 Using cached quiz for: {url}")
            return existing
        
        # Scrape Wikipedia
        logger.info(f"🔍 Scraping: {url}")
        title, summary, sections, raw_html = scrape_wikipedia(url)
        
        # Generate quiz with LLM
        logger.info(f"🤖 Generating quiz...")
        quiz_data = generate_quiz(summary, title)
        
        # Extract entities (optional enhancement)
        entities = extract_key_entities(summary)
        
        # Prepare data for storage
        article_data = {
            "url": url,
            "title": title,
            "summary": summary[:1000],  # Limit summary to 1000 chars
            "key_entities": entities,
            "sections": sections,
            "quiz": quiz_data.get("quiz", []),
            "related_topics": quiz_data.get("related_topics", []),
        }
        
        # Store in file
        result = save_quiz(article_data)
        
        # Return response
        return result
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history():
    """
    Get list of all previously generated quizzes
    """
    try:
        quizzes = get_all_quizzes()
        return [
            QuizHistoryItem(
                id=q.get("id"),
                url=q.get("url"),
                title=q.get("title"),
                created_at=q.get("created_at")
            )
            for q in quizzes
        ]
    except Exception as e:
        logger.error(f"❌ Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quiz/{quiz_id}")
async def get_quiz_details(quiz_id: int):
    """
    Get full quiz details by ID (for modal in Tab 2)
    """
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return quiz


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

