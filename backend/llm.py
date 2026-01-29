import google.generativeai as genai
import json
import os
import logging
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configure_gemini():
    """Configure Gemini API with API key from environment"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)


def generate_quiz(text: str, title: str = "") -> Dict:
    """
    Generate quiz questions from Wikipedia article text using Gemini
    
    Args:
        text: Article content
        title: Article title (for context)
        
    Returns:
        Dictionary with quiz questions and related topics
    """
    
    configure_gemini()
    
    prompt = f"""
You are an expert quiz generator. Based on the following Wikipedia article text, generate a structured JSON response with quiz questions and related topics.

IMPORTANT RULES:
1. Generate EXACTLY 5-7 multiple choice questions
2. All questions MUST be answerable from the provided text
3. Each question must have 4 options (A, B, C, D)
4. Difficulty levels: "easy" (1-2 questions), "medium" (2-3), "hard" (1-2)
5. Explanations must cite the specific section or fact
6. Related topics should be 3-5 Wikipedia topics mentioned in the text

ARTICLE TITLE: {title}

ARTICLE TEXT:
{text[:3000]}

Return ONLY valid JSON (no markdown, no explanation) in this exact format:
{{
  "quiz": [
    {{
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Correct Option",
      "difficulty": "easy|medium|hard",
      "explanation": "Why this is correct based on the text"
    }}
  ],
  "related_topics": ["Topic1", "Topic2", "Topic3"]
}}
"""
    
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        result = json.loads(response_text)
        logger.info(f"✅ Generated quiz with {len(result.get('quiz', []))} questions")
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Failed to parse LLM response as JSON: {e}")
        raise Exception("LLM returned invalid JSON")
    except Exception as e:
        logger.error(f"❌ LLM generation failed: {e}")
        raise Exception(f"Failed to generate quiz: {e}")
